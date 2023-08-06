
def linreg_mle(y, X, algorithm='Nelder-Mead', debug=False):
    """MLE for Linear Regression Model

    Parameters:
    -----------
    y : ndarray
        target variable with N observations

    X : ndarray
        The <N x C> design matrix with C independent
        variables, features, factors, etc.

    algorithm : str
        Optional. Default 'Nelder-Mead' (Simplex).
        The algorithm used in scipy.optimize.minimize

    debug : bool
        Optional.

    Returns:
    --------
    beta : ndarray
        Estimated regression coefficients.

    results : scipy.optimize.optimize.OptimizeResult
        Optional. If debug=True then only scipy's
        optimization result variable is returned.

    """
    import numpy as np
    import scipy.stats as sstat
    import scipy.optimize as sopt

    def objective_nll_linreg(theta, y, X):
        yhat = np.dot(X, theta[:-1])  # =X*beta
        return -1.0 * sstat.norm.logpdf(y, loc=yhat, scale=theta[-1]).sum()

    # check eligible algorithm
    if algorithm not in ('Nelder-Mead', 'CG', 'BFGS'):
        raise Exception('Optimization Algorithm not supported.')

    # set start values
    theta0 = np.ones((X.shape[1] + 1, ))

    # run solver
    results = sopt.minimize(
        objective_nll_linreg,
        theta0,
        args=(y, X),
        method=algorithm,
        options={'disp': False})

    # debug?
    if debug:
        return results

    # done
    return results.x[:-1]
