
def corr_rank(x, axis=0):
    """Spearman's Rho as Rank Correlation Matrix(for ordinal data)

    Parameters
    ----------
    x : ndarray
        data set

    axis : int, optional
        Variables as columns is the default (axis=0).
        If variables are in the rows use axis=1

    Returns
    -------
    r : ndarray
        Correlation Matrix

    p : ndarray
        p-values
    """
    # load modules
    from scipy.stats import spearmanr
    import numpy as np
    import oxyba as ox
    import warnings

    # transpose if axis<>0
    if axis is not 0:
        x = x.T

    # read dimensions and
    n, c = x.shape

    # check if enough variables provided
    if c < 2:
        raise Exception("Only " + str(c) +
                        " variables provided. At least 2 variables required")
    #
    # check if ordinal or send warning message
    for i in range(x.shape[1]):
        flag, msg = ox.isordinal(x[:, i])
        if not flag:
            warnings.warn(msg)

    # allocate variables
    r = np.ones((c, c))
    p = np.zeros((c, c))

    # compute each (i,j)-th correlation
    for i in range(0, c):
        for j in range(i + 1, c):
            r[i, j], p[i, j] = spearmanr(x[:, i], x[:, j])
            r[j, i] = r[i, j]
            p[j, i] = p[i, j]

    # done
    return r, p
