
def features_check_singular(X, tol=1e-8):
    """Checks if a set of features/variables X result in a
    ill-conditioned matrix dot(X.T,T)

    Parameters:
    -----------
    X : ndarray
        An NxM array with N observations (rows)
        and M features/variables (columns).

        Note: Make sure that X variables are all normalized or
        or scaled, e.g.
            X = sklearn.preprocessing.normalize(rawdata, norm='l2')

    tol : float
        Threshold when to consider a Singular Value s_k (U*S*V^T of SVD)
        is considered to small s_k<tol. The Default is tol=1e-8.

    Returns:
    --------
    flag : bool
        True if the X leads to singular matrix dot(X.T,T), or
        False if X does not not lead to singular matrix.

    num : int
        Number of Singular Values that failed the s_k<tol test

    s : ndarray
        The Singular Values computed by numpy.linalg.svd

    Usage:
    ------
    * flag. During Forward-Selection check if an newly added
      variable causes an ill-conditioned matrix.
    * num. Get an indication how many variables still needs to
      be eliminated during Backward-Selection
    """
    import numpy as np
    _, s, _ = np.linalg.svd(np.dot(X.T, X))
    failed = s < tol
    flag = True if np.any(failed) else False
    return flag, failed.sum(), s
