
def linreg_ols_lu(y, X):
    """Linear Regression, OLS, by solving linear equations and LU decomposition

    Properties
    ----------
    * based on LAPACK's _gesv what applies LU decomposition
    * avoids using python's inverse functions
    * should be stable
    * no overhead or other computations

    Example:
    --------
        beta = linreg_ols_lu(y,X)

    Links:
    ------
    * http://oxyba.de/docs/linreg_ols_lu

    """
    import numpy as np
    try:  # solve OLS formula
        return np.linalg.solve(np.dot(X.T, X), np.dot(X.T, y))
    except np.linalg.LinAlgError:
        print("LinAlgError: X*X' is singular or not square.")
        return None
