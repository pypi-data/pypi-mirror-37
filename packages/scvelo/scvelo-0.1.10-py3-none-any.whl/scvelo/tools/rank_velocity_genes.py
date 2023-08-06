from ..logging import logg, settings
from scipy.sparse import issparse
from scanpy.preprocessing.simple import filter_genes_dispersion
import numpy as np


def get_mean_var(X, ignore_zeros=False, perc=None):
    data = X.data if issparse(X) else X
    mask_nans = np.isnan(data) | np.isinf(data) | np.isneginf(data)

    n_nonzeros = (X != 0).sum(0)
    n_counts = n_nonzeros if ignore_zeros else X.shape[0]

    if mask_nans.sum() > 0:
        if issparse(X):
            data[np.isnan(data) | np.isinf(data) | np.isneginf(data)] = 0
            n_nans = n_nonzeros - (X != 0).sum(0)
        else:
            X[mask_nans] = 0
            n_nans = mask_nans.sum(0)
        n_counts -= n_nans

    if perc is not None:
        if isinstance(perc, int): perc = [perc, 100] if perc < 50 else [0, perc]
        lb, ub = np.percentile(data, perc)
        data = np.clip(data, lb, ub)

    mean = (X.sum(0) / n_counts).A1 if issparse(X) else X.sum(0) / n_counts
    mean_sq = (X.multiply(X).sum(0) / n_counts).A1 if issparse(X) else np.multiply(X, X).sum(0) / n_counts
    var = (mean_sq - mean ** 2) * (X.shape[0] / (X.shape[0] - 1))

    mean[np.isnan(mean)] = 0
    var[np.isnan(var)] = 0
    return mean, var


def select_groups(adata, groups='all', key='louvain'):
    """Get subset of groups in adata.obs[key].
    """
    categories = adata.obs[key].cat.categories
    groups_masks = np.array([categories[i] == adata.obs[key].values for i, name in enumerate(categories)])
    if groups == 'all':
        groups = categories.values
    else:
        groups_ids = [np.where(categories.values == name)[0][0] for name in groups]
        groups_masks = groups_masks[groups_ids]
        groups = categories[groups_ids].values
    return groups, groups_masks


def rank_velocity_genes(data, groupby=None, groups='all', n_genes=10, min_counts=None, min_r2=None, min_dispersion=None,
                        method='t-test_overestim_var', use_raw=True, copy=False):
    """Rank genes for characterizing groups according to unspliced/spliced correlation and differential expression.
    Parameters
    ----------
    data : :class:`~anndata.AnnData`
        Annotated data matrix.
    groupby : `str`
        The key of the observations grouping to consider.
    use_raw : `bool`, optional (default: `True`)
        Use `raw` attribute of `adata` if present.
    groups : `str`, `list`, optional (default: `'all'`)
        Subset of groups, e.g. `['g1', 'g2', 'g3']`, to which comparison shall
        be restricted. If not passed, a ranking will be generated for all
        groups.
    n_genes : `int`, optional (default: 100)
        The number of genes that appear in the returned tables.
    method : {'t-test', 't-test_overestim_var'} (default: 't-test_overestim_var')
        If 't-test' uses t-test, if 't-test_overestim_var' overestimates variance of each group.

    Returns
    -------
    Updates `adata` with the following fields.
    names : structured `np.ndarray` (`.uns['rank_genes_groups']`)
        Structured array to be indexed by group id storing the gene
        names. Ordered according to scores.
    scores : structured `np.ndarray` (`.uns['rank_genes_groups']`)
        Structured array to be indexed by group id storing the score for each
        gene for each group. Ordered according to scores.

    """
    adata = data.copy() if copy else data
    logg.info('ranking velocity genes', r=True)
    if method not in {'t-test', 't-test_overestim_var'}: raise ValueError('Method not available.')

    if True:
        n_counts = (adata.layers['unspliced'] > 0).sum(0)
        n_counts = n_counts.A1 if issparse(adata.layers['unspliced']) else n_counts
        min_counts = np.percentile(n_counts, 80) if min_counts is None else min_counts
        filter_counts = n_counts > min_counts

        r2 = adata.var.velocity_r2
        min_r2 = np.percentile(r2[r2 > 0], 80) if min_r2 is None else min_r2
        filter_r2 = r2 > min_r2

        dispersions = adata.var.dispersions_norm if 'dispersions_norm' in adata.var.keys() \
            else filter_genes_dispersion(adata.X)['dispersions_norm']
        min_dispersion = np.percentile(dispersions, 20) if min_dispersion is None else min_dispersion
        filter_dispersions = dispersions > min_dispersion

        idx_sub = filter_counts & filter_r2 & filter_dispersions
        if 'velocity_genes' in adata.var.keys(): idx_sub = idx_sub & adata.var['velocity_genes']

    else:
        tmp_filter = adata.layers['velocity'] > np.percentile(adata.layers['velocity'], 95, axis=0)
        std = np.empty(adata.n_vars, dtype=np.float32)
        for i in range(adata.n_vars):
            std[i] = adata.obsm['X_' + basis][tmp_filter[:, i]].std(0).mean()
        idx_random = np.random.choice(adata.n_obs, size=int(adata.n_obs / 10), replace=False)
        threshold = adata.obsm['X_' + basis][idx_random].std(0).mean() - std.std()  # p=0.1
        if 'velocity_genes' in adata.var.keys(): std[~adata.var['velocity_genes']] = np.inf
        idx_sub = std < threshold
        n_counts = -std

    adata_sub = adata[:, idx_sub]
    if groupby is None:
        return np.array(adata_sub.var_names[np.argsort(n_counts[idx_sub])[::-1][:n_genes]])
    else:
        X = adata_sub.raw.X if adata_sub.raw is not None and use_raw else adata_sub.X
        if n_genes > X.shape[1]: n_genes = X.shape[1]

        if isinstance(groups, list) and isinstance(groups[0], int): groups = [str(n) for n in groups]
        groups, groups_masks = select_groups(adata_sub, groups, groupby)
        n_groups = groups_masks.shape[0]
        sizes = groups_masks.sum(1)

        mean, var = np.zeros((n_groups, X.shape[1])), np.zeros((n_groups, X.shape[1]))
        for i, mask in enumerate(groups_masks): mean[i], var[i] = get_mean_var(X[mask])

        # test each against the union of all other groups
        rankings_gene_names, rankings_gene_scores, rankings_gene_r2 = [], [], []
        for i in range(n_groups):
            mask_rest = ~groups_masks[i]
            mean_rest, var_rest = get_mean_var(X[mask_rest])
            size_rest = mask_rest.sum() if method == 't-test' else sizes[i]

            scores = (mean[i] - mean_rest) / np.sqrt(var[i] / sizes[i] + var_rest / size_rest)
            scores[np.isnan(scores)] = 0

            # equivalent to but much faster than np.argsort(scores)[-10:]
            idx = np.argpartition(scores, -n_genes)[-n_genes:]
            idx = idx[np.argsort(scores[idx])[::-1]]

            rankings_gene_names.append(adata_sub.var_names[idx].values)
            rankings_gene_scores.append(scores[idx])
            rankings_gene_r2.append(adata_sub.var['velocity_r2'][idx])

        rankings_gene_names = np.array([list(n) for n in rankings_gene_names])
        rankings_gene_scores = np.array([list(n) for n in rankings_gene_scores])
        rankings_gene_gammas = np.array([list(n) for n in rankings_gene_r2])

        #rankings_gene_names = np.rec.fromarrays([n for n in rankings_gene_names], dtype=[(rn, 'U50') for rn in groups])
        #rankings_gene_scores = np.rec.fromarrays([n for n in rankings_gene_scores], dtype=[(rn, 'float32') for rn in groups])
        #rankings_gene_gammas = np.rec.fromarrays([n for n in rankings_gene_gammas], dtype=[(rn, 'float32') for rn in groups])

        key = 'rank_velocity_genes'
        if key not in adata.uns.keys(): adata.uns[key] = {}
        adata.uns[key] = {'groups': groups, 'names': rankings_gene_names,
                          'scores': rankings_gene_scores.round(0), 'r2': rankings_gene_gammas.round(2)}

        logg.info('    finished', time=True, end=' ' if settings.verbosity > 2 else '\n')
        logg.hint(
            'added to `.uns`\n'
            '    \'' + key + '\', sorted np.recarray to be indexed by group ids\n')

        return adata if copy else None
