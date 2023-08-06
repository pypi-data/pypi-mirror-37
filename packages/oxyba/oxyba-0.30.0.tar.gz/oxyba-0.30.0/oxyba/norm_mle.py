
def norm_mle(data, algorithm='Nelder-Mead', debug=False):
    """Estimate Mean and Std.Dev. of the Normal Distribution

    Parameters:
    -----------
    data : list, tuple, ndarray
        vector with samples, observations that are
        assumed to follow a Normal distribution.

    algorithm : str
        Optional. Default 'Nelder-Mead' (Simplex).
        The algorithm used in scipy.optimize.minimize

    debug : bool
        Optional.

    Returns:
    --------
    mu : float
        Mean, 1st moment, location parameter of the
            Normal distribution.

    sd : float
        Standard Deviation, 2nd moment, scale parameter
            of the Normal distribution

    results : scipy.optimize.optimize.OptimizeResult
        Optional. If debug=True then only scipy's
        optimization result variable is returned.

    """
    import scipy.stats as sstat
    import scipy.optimize as sopt

    def objective_nll_norm_uni(theta, data):
        return -1.0 * sstat.norm.logpdf(
            data, loc=theta[0], scale=theta[1]).sum()

    # check eligible algorithm
    if algorithm not in ('Nelder-Mead', 'CG', 'BFGS'):
        raise Exception('Optimization Algorithm not supported.')

    # set start values
    theta0 = [1.0, 1.0]  # mu and sigma

    # run solver
    results = sopt.minimize(
        objective_nll_norm_uni, theta0,
        args=(data),
        method=algorithm,
        options={'disp': False})

    # debug?
    if debug:
        return results

    # done
    return results.x[0], results.x[1]
