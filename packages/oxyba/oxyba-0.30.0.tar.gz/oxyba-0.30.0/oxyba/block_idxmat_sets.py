
def block_idxmat_sets(idxmat, b):
    """Reshapes idxmat into the idx vectors for the training set and validation set

    Parameters:
    -----------
    idxmat : ndarray
        Matrix with N shuffled row indicies assigned to K blocks/columns
        from the oxyba.block_idxmat_shuffle function

    b : int
        The id of the current validation block b=[0,1,...,K-1]

    Returns:
    --------
    idx_train : ndarray
        Vector with row indicies of the current training blocks,
        i.e. all blocks [0,1,...,K-1] except the b-th block.
        The vector contains int(N/K)*(K-1) elements.

    idx_valid : ndarray
        Vector with row indicies of the current validation block "b".
        The vector contains int(N/K) elements.

    Example:
    --------
        K = idxmat.shape[1]
        for b in range(K):
            idx_train, idx_valid = block_idxmat_sets(idxmat, b)
            ...
    """
    import numpy as np
    idx_train = idxmat[:, [c for c in range(idxmat.shape[1]) if c is not b]]
    idx_train = idx_train.reshape((np.prod(idx_train.shape),))
    return idx_train, idxmat[:, b]
