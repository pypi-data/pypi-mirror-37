"""
Module for computing variance estimates for 5C interaction data.
"""

import numpy as np
import scipy.stats as stats
from scipy.ndimage import generic_filter

from lib5c.algorithms.variance_legacy.dispersion import estimate_mle_dispersion_variance, \
    estimate_pixel_wise_disp_across_reps, dispersion_to_variance
from lib5c.util.parallelization import parallelize_regions
from lib5c.util.optimization import quadratic_log_log_fit
from lib5c.util.lowess import lowess_fit, group_fit
from lib5c.util.counts import flatten_obs_and_exp, flatten_counts_to_list, \
    unflatten_counts_from_list
from lib5c.util.grouping import group_obs_by_exp
from lib5c.util.donut import donut_footprint
from lib5c.util.distributions import convert_parameters


def estimate_variance_across_reps(obs_counts_superdict, exp_counts,
                                  model='lognorm', min_obs=2, min_disp=1e-7,
                                  x_unit='exp', y_unit='disp', logx=True,
                                  logy=True, fitter='group', pixelmap=None):
    """
    Computes variance estimates across replicates.

    First obtains pixel-wise MLE dispersion estimates via
    ``lib5c.algorithms.dispersion.estimate_pixel_wise_disp_across_reps()``, then
    fits a lowess relationship between ``x_unit`` and ``y_unit`` on the scale
    specified by ``logx`` and ``logy``.

    Parameters
    ----------
    obs_counts_superdict : dict of dict of np.ndarray
        Observed data for at least two replicates. The outer dict's keys are
        replicate names as strings. The inner dict's keys are region names as
        strings. The inner dict's values are square, symmetric arrays of the
        observed values.
    exp_counts : dict of np.ndarray
        Expected data for just this one replicate. Keys are region names as
        strings, values are square symmetric arrays of the expected values.
    model : {'lognorm', 'norm', 'nbinom'}
        The model under which to estimate the pixel-wise variance. This changes
        the meaning of "disp" in subsequent kwargs.
    min_obs : float
        Points with observed values below this threshold in any replicate will
        be excluded from the estimation, and will have a variance estimate of
        ``nan``.
    min_disp : float
        When ``model='nbinom'``, this sets the minimum value of the negative
        binomial dispersion parameter. When ``model='lognormal'``, this sets the
        minimum value of the variance of logged observed counts. When
        ``model='norm'``, this sets the minimum value of the variance of
        observed counts. Either way, points that fall below the minimum will be
        excluded from relationship fitting.
    x_unit : {'dist', 'exp'}
        The x-unit to fit the variance relationship against.
    y_unit : {'disp', 'var'}
        The y-unit to fit the variance relationship against. When
        ``model='nbinom'``, "disp" refers to the negative binomial dispersion
        parameter. When ``model='lognorm'``, "disp" refers to the variance
        parameter of the normal distribution describing the logarithm of the
        observed counts. When ``model='norm'``, "disp" falls back to referring
        to the variance of the observed counts (equivalent to "var").
    logx, logy : bool
        Pass True to fit the variance relationship on the scale of ``log(x)``
        and/or ``log(y)``.
    fitter : {'group', 'lowess'}
        Specifies what fitting approach to use, either a group-based sliding
        window fitter or lowess.
    pixelmap : dict of list of dict, optional
        Pass a pixelmap to return the variance estimates as a counts dict. If
        not passed, only the fitted variance relationship function will be
        returned.

    Returns
    -------
    fit : function
        The fitted variance relationship function.
    nll_mle, nll_fit : float
        The negative log-likelihoods of the data under the MLE-estimated and
        fitted variance models, respectively.
    var_counts : dict of np.ndarray, optional
        The variance estimates as a counts dict. Only returned if ``pixelmap``
        is passed.

    Notes
    -----
    This function obtains the final variance estimates by first estimating
    dispersion values from the fitted relationship (even if ``y_unit == 'var'``)
    and then applying those dispersion values to the expected value (not the
    pixel-wise mean that the dispersions are estimated from).

    This function returns a replicate-specific variance estimate, even though
    observed values are passed from multiple replicates. This is because if
    ``x_unit == 'exp'``, then the relationship is fitted against the
    replicate-specific expected value. Additionally, the final estimated
    dispersion values are always applied to the replicate-specific expected
    value, even when ``x_unit == 'dist'``.
    """
    exp, dist, mean_mle, disp_mle, var_mle, idx, idx_od, matrix, region_order =\
        estimate_pixel_wise_variance(
            obs_counts_superdict, exp_counts, model=model, min_obs=min_obs,
            min_disp=min_disp)

    # decide how to fit
    if x_unit == 'dist':
        x = dist
    elif x_unit == 'exp':
        x = exp
    else:
        raise ValueError('unknown x_unit %s' % x_unit)
    if y_unit == 'disp':
        y = disp_mle
    elif y_unit == 'var':
        y = var_mle
    else:
        raise ValueError('unknown y_unit %s' % y_unit)

    # perform the fit and get variance estimates
    fitters = {'lowess': lowess_fit, 'group': group_fit}
    fit = fitters[fitter](x[idx_od], y[idx_od], logx=logx, logy=logy)
    y_hat = fit(x)
    var = np.tile(np.nan, idx.shape)
    if y_unit == 'disp':
        if model == 'lognorm':
            mean = np.log(exp) - y_hat/2  # convert exp to mean of log counts
            var[idx] = (np.exp(y_hat)-1) * np.exp(2*mean + y_hat)
        elif model == 'nbinom':
            var[idx] = dispersion_to_variance(y_hat, exp)
        else:
            # no implementation for conversion implies that disp = var
            var[idx] = y_hat
    else:
        var[idx] = y_hat

    # compute NLL of fitted variances compared to MLE variances
    models = {
        'lognorm': (stats.norm, True, 'logpdf'),
        'norm': (stats.norm, False, 'logpdf'),
        'nbinom': (stats.nbinom, False, 'logpmf')
    }
    var_sources = {
        'mle': var_mle[idx_od],
        'fit': var[idx][idx_od]
    }
    dist_gen, log, fn = models[model]
    transform = np.log if log else np.floor if fn == 'logpmf' else lambda z: z
    nll = {name: -np.sum(getattr(dist_gen(
        *convert_parameters(mean_mle[idx_od], var_source, dist_gen,
                            log=log)), fn)(transform(matrix[:, idx_od])))
           for name, var_source in var_sources.items()}

    if pixelmap is None:
        return fit, nll['mle'], nll['fit']

    # repackage variance estimates into counts dict
    var_counts = unflatten_counts_from_list(var, region_order, pixelmap)

    return fit, nll['mle'], nll['fit'], var_counts


def estimate_pixel_wise_variance(obs_counts_superdict, exp_counts,
                                 model='lognorm', min_obs=2, min_disp=1e-7):
    """
    Computes pixel-wise variance and disperion across replicates.

    Parameters
    ----------
    obs_counts_superdict : dict of dict of np.ndarray
        Observed data for at least two replicates. The outer dict's keys are
        replicate names as strings. The inner dict's keys are region names as
        strings. The inner dict's values are square, symmetric arrays of the
        observed values.
    exp_counts : dict of np.ndarray
        Expected data for just this one replicate. Keys are region names as
        strings, values are square symmetric arrays of the expected values.
    model : {'lognorm', 'norm', 'nbinom'}
        The model under which to estimate the pixel-wise variance. This changes
        the meaning of "disp" in subsequent kwargs.
    min_obs : float
        Points with observed values below this threshold in any replicate will
        be excluded from the estimation, and will have a variance estimate of
        ``nan``.
    min_disp : float
        When ``model='nbinom'``, this sets the minimum value of the negative
        binomial dispersion parameter. When ``model='lognormal'``, this sets the
        minimum value of the variance of logged observed counts. When
        ``model='norm'``, this sets the minimum value of the variance of
        observed counts. Either way, points that fall below the minimum will be
        excluded from relationship fitting.

    Returns
    -------
    exp, dist, mean, disp_mle, var_mle, idx, idx_od : np.ndarray
        The first five are parallel vectors representing qualities of the points
        that satisfy the criteria for estimation. The sixth is a boolean index
        into the flattened original counts dict which is True at points that
        were included into the parallel vectors. The seventh is a boolean index
        into the parallel vectors which is True at points that pass the minimum
        dispersion threshold.
    matrix : np.ndarray
        The matrix of the observed counts. Rows correspond to replicates of the
        counts superdict, and columns correspond to entries in the flattened
        counts vector where ``idx`` is True.
    region_order : list of str
        The region order with which the counts dicts were flattened to make the
        parallel vectors.
    """
    # flatten everything, including distance values
    rep_order = obs_counts_superdict.keys()
    region_order = exp_counts.keys()
    matrix = np.array([flatten_counts_to_list(obs_counts_superdict[rep],
                                              region_order=region_order,
                                              discard_nan=False)
                       for rep in rep_order])
    exp = flatten_counts_to_list(exp_counts, region_order=region_order,
                                 discard_nan=False)
    dist_counts = {region: np.array([[np.abs(i - j)
                                      for i in range(len(exp_counts[region]))]
                                     for j in range(len(exp_counts[region]))])
                   for region in region_order}
    dist = flatten_counts_to_list(dist_counts, region_order=region_order,
                                  discard_nan=False)

    # select a subset of pixels
    idx = np.isfinite(matrix).all(axis=0) & np.all(matrix >= min_obs, axis=0) &\
        np.isfinite(exp) & (dist > 0) & (exp > 0)
    matrix = matrix[:, idx]
    exp = exp[idx]
    dist = dist[idx]

    # perform pixel-wise MLE step
    # after this block all of mean_mle, disp_mle, var_mle, and idx_od exist
    # disp_mle refers to a generic dispersion parameter for any distribution
    # idx_od refers to points that pass the min_disp threshold
    if model == 'lognorm':
        log_matrix = np.log(matrix)
        mu_mle = np.mean(log_matrix, axis=0)
        disp_mle = np.var(log_matrix, axis=0)
        idx_od = disp_mle > min_disp
        disp_mle[~idx_od] = min_disp
        mean_mle = np.exp(mu_mle + disp_mle/2)
        var_mle = (np.exp(disp_mle) - 1) * np.exp(2 * mu_mle + disp_mle)
    elif model == 'norm':
        mean_mle = np.mean(matrix, axis=0)
        var_mle = np.var(matrix, axis=0)
        idx_od = var_mle > min_disp
        var_mle[~idx_od] = min_disp
        disp_mle = var_mle
    elif model == 'nbinom':
        disp_mle, mean_mle, idx_od = estimate_pixel_wise_disp_across_reps(
            matrix, min_disp=min_disp)
        var_mle = dispersion_to_variance(disp_mle, mean_mle)
    else:
        raise ValueError('unknown model %s' % model)

    return exp, dist, mean_mle, disp_mle, var_mle, idx, idx_od, matrix, \
        region_order


@parallelize_regions
def estimate_variance(obs, exp, method='disp', **kwargs):
    """
    Convenience function for estimating the variance using any of a variety of
    available methods.

    Parameters
    ----------
    obs : np.ndarray
        Regional matrix of the observed values.
    exp : np.ndarray
        Regional matrix of the expected values.
    method : {'disp', 'mvr', 'vst', 'local', 'local_vst', 'poisson'}
        The method by which the variance should be estimated.
    kwargs : additional keyword arguments
        Will be passed to the selected ``estimate_*_variance()`` function.

    Returns
    -------
    np.ndarray
        Regional matrix of variances.
    """
    if method == 'disp':
        return estimate_mle_dispersion_variance(obs, exp, **kwargs)
    elif method == 'mvr':
        return estimate_mvr_variance(obs, exp, **kwargs)
    elif method == 'vst':
        return estimate_vst_variance(obs, exp, **kwargs)
    elif method == 'local':
        return estimate_local_variance(obs, exp, vst=False, **kwargs)
    elif method == 'local_vst':
        return estimate_local_variance(obs, exp, vst=True, **kwargs)
    elif method == 'poisson':
        return exp
    else:
        raise ValueError('unrecognized variance estimation method: %s' % method)


def estimate_global_mvr_variance(obs_counts, exp_counts, num_groups=100,
                                 group_fractional_tolerance=0.1,
                                 exclude_offdiagonals=5):
    """
    Estimates the variance using a single mean-variance relationship shared
    across all regions.

    Parameters
    ----------
    obs_counts : dict of np.ndarray
        Counts dict of observed values.
    exp_counts : dict of np.ndarray
        Counts dict of expected values.
    num_groups : int
        The number of groups to fit the MVR to.
    group_fractional_tolerance : float
        The width of each group, specified as a fractional tolerance in the
        expected value.
    exclude_offdiagonals : int
        Exclude this many off-diagonals from the estimation. Pass 0 to exclude
        only the exact diagonal. Pass -1 to exclude nothing.

    Returns
    -------
    dict of np.ndarray
        The counts dict containing the estimated variances.
    """
    exps, groups = group_obs_by_exp(
        obs_counts, exp_counts,
        num_groups=num_groups,
        group_fractional_tolerance=group_fractional_tolerance,
        exclude_offdiagonals=exclude_offdiagonals)
    vars = np.array([np.nanvar(group) for group in groups])
    mvr = quadratic_log_log_fit(exps, vars)
    return {region: mvr(exp_counts[region]) for region in exp_counts}


@parallelize_regions
def estimate_mvr_variance(obs, exp, num_groups=100,
                          group_fractional_tolerance=0.1,
                          exclude_offdiagonals=5):
    """
    Estimates the variance using a mean-variance relationship.

    Parameters
    ----------
    obs : np.ndarray
        Regional matrix of the observed values.
    exp : np.ndarray
        Regional matrix of the expected values.
    num_groups : int
        The number of groups to fit the MVR to.
    group_fractional_tolerance : float
        The width of each group, specified as a fractional tolerance in the
        expected value.
    exclude_offdiagonals : int
        Exclude this many off-diagonals from the estimation. Pass 0 to exclude
        only the exact diagonal. Pass -1 to exclude nothing.

    Returns
    -------
    np.ndarray
        Regional matrix of variances.
    """
    exps, groups = group_obs_by_exp(
        obs, exp,
        num_groups=num_groups,
        group_fractional_tolerance=group_fractional_tolerance,
        exclude_offdiagonals=exclude_offdiagonals)
    vars = np.array([np.nanvar(group) for group in groups])
    mvr = quadratic_log_log_fit(exps, vars)
    return mvr(exp)


@parallelize_regions
def estimate_vst_variance(obs, exp, dist_gen=stats.logistic):
    """
    Estimates the variance using a variance-stabilizing transform.

    Parameters
    ----------
    obs : np.ndarray
        Regional matrix of the observed values.
    exp : np.ndarray
        Regional matrix of the expected values.
    dist_gen : scipy.stats.rv_generic
        The distribution to use to estimate the variance of the VST'd data.

    Returns
    -------
    np.ndarray
        Regional matrix of variances.
    """
    flat_obs, flat_exp = flatten_obs_and_exp(obs, exp, log=True)
    stabilized_variance = dist_gen(*dist_gen.fit(flat_obs-flat_exp))\
        .stats(moments='v')
    return np.ones_like(exp) * stabilized_variance


@parallelize_regions
def estimate_local_variance(obs, exp, p=5, w=15, vst=False):
    """
    Estimates the variance using a local donut window.

    Parameters
    ----------
    obs : np.ndarray
        Regional matrix of the observed values.
    exp : np.ndarray
        Regional matrix of the expected values.
    w : int
        The outer radius of the donut window to use.
    p : int
        The inner radius of the donut window to use.
    vst : bool
        Pass True to apply a VST before estimating the local variance.

    Returns
    -------
    np.ndarray
        Regional matrix of variances.
    """
    if vst:
        obs = np.log(obs + 1)
        exp = np.log(exp + 1)
    return generic_filter(
        obs - exp,
        lambda x: np.nansum(x**2) / (np.sum(np.isfinite(x))-1),
        footprint=donut_footprint(p, w), mode='constant', cval=np.nan
    )
