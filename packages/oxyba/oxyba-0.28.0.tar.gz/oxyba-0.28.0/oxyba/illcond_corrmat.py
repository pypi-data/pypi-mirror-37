
def illcond_corrmat(D, random_state=None):
    """Generate a <D x D> ill-conditioned correlation matrix
    with random coefficients

    Parameters:
    -----------
    D : int
        Dimension of the matrix

    Return:
    -------
    cmat : ndarray
        DxD matrix with +1 as diagonal elements,
        mirrored random numbers [-1,+1].
    """
    import numpy as np
    if random_state:
        np.random.seed(random_state)
    tmp = np.minimum(1., np.maximum(
        -1., 2 * np.random.uniform(size=(D, D)) - 1.0))
    tmp = np.triu(tmp, k=1)
    return np.eye(D) + tmp + tmp.T
