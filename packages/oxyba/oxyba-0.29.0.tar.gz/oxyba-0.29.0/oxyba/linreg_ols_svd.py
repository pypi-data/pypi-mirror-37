
def linreg_ols_svd(y, X, rcond=1e-15):
    """Linear Regression, OLS, inv by SVD

    Properties
    ----------
    * Numpy's lstsq is based on LAPACK's _gelsd what applies SVD
    * SVD inverse might be slow (complex Landau O)
    * speed might decline during forward selection
    * no overhead or other computations

    Example:
    --------
        beta = lin_ols_svd(y,X)
    """
    import numpy as np
    try:  # solve OLS formula
        beta, _, _, singu = np.linalg.lstsq(b=y, a=X, rcond=rcond)
    except np.linalg.LinAlgError:
        print("LinAlgError: computation does not converge.")
        return None

    # check singu
    if np.any(singu < 0.0):
        print("Error: A singular value of X is numerically not well-behaved.")
        return None

    # return estimated model parameters
    return beta
