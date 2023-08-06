
def rand_bivar(X, rho):
    """Transform two unrelated random variables into correlated bivariate data

    X : ndarray
        two univariate random variables
        with N observations as <N x 2> matrix

    rho : float
        The Pearson correlations coefficient
        as number between [-1, +1]
    """
    import numpy as np
    Y = np.empty(X.shape)
    Y[:, 0] = X[:, 0]
    Y[:, 1] = rho * X[:, 0] + np.sqrt(1.0 - rho**2) * X[:, 1]
    return Y
