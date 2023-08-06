
def rand_chol(X, rho):
    """Transform C uncorrelated random variables into correlated data

    X : ndarray
        C univariate correlated random variables
        with N observations as <N x C> matrix

    rho : ndarray
        Correlation Matrix (Pearson method) with
        coefficients between [-1, +1]
    """
    import numpy as np
    return np.dot(X, np.linalg.cholesky(rho).T)
