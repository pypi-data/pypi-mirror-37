
def linreg_ridge_gd(y, X, lam, algorithm='L-BFGS-B', debug=False):
    """Ridge Regression with Gradient Optimization methods

    Parameters:
    -----------
    y : ndarray
        target variable with N observations

    X : ndarray
        The <N x C> design matrix with C independent
        variables, features, factors, etc.

    algorithm : str
        Optional. The algorithm used in scipy.optimize.minimize
        and 'L-BFGS-B' (Limited BFGS) as default.

        Eligible algorithms are 'CG', 'BFGS', 'Newton-CG', 'L-BFGS-B',
        'TNC', and 'SLSQP' as these use the supplied gradient function.

        This is an unconstrained optimization problem. Thus, the 'L-BFGS-B',
        'TNC' and 'SLSQP' options does not make use of constraints.

        'TNC' (Truncated Newton) seems to be suited to for larger datasets
        and 'L-BFGS-B' (Limited BFGS) if computing powever becomes an issue.

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
    import scipy.optimize as sopt

    def objective_pssr(theta, y, X, lam):
        return np.sum((y - np.dot(X, theta))**2) + lam * np.sum(theta**2)

    def gradient_pssr(theta, y, X, lam):
        return -2.0 * np.dot(X.T, (y - np.dot(X, theta))) + 2.0 * lam * theta

    # check eligible algorithm
    if algorithm not in ('CG', 'BFGS', 'Newton-CG',
                         'L-BFGS-B', 'TNC', 'SLSQP'):
        raise Exception('Optimization Algorithm not supported.')

    # set start values
    theta0 = np.ones((X.shape[1],))

    # run solver
    results = sopt.minimize(
        objective_pssr,
        theta0,
        jac=gradient_pssr,
        args=(y, X, lam),
        method=algorithm,
        options={'disp': False})

    # debug?
    if debug:
        return results

    # done
    return results.x
