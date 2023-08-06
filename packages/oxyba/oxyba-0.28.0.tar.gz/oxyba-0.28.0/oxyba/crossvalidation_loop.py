

def crossvalidation_loop(fitfunc, evalfunc, data,
                         K=None, idxmat=None, random_state=None):
    """Cross Validation

    Parameters:
    -----------
    fitfunc : function
        A function that wraps the model/algorithm, has 1 data
        variable as input argument, and returns the estimated
        coefficients, model parameters, weights, etc.

    evalfunc : function
        A function pointer to an evaluation, fitness, cost, etc.
        function that returns an error, score, etc. metric

    data : ndarray
        The data i.e. target variable and predictors in one
        common python variable, e.g. `data=np.c_[y, X]`

    K : int
        Number of blocks

    idxmat : ndarray
        See below. If provided the block are not shuffled again.

    random_state : int
        For oxyba.block_idxmat_shuffle

    Returns:
    --------
    errors : ndarray
        The CV errors per validation block
        (i.e. the result of the fitness function fo reach block)

    coeffs : ndarray
        The estimated coefficients for each training subsample
        (i.e. all blocks except the validation blocks)

    idxmat : ndarray
        The shuffled row indicies for each block. The row indicies
        assigned to each block are stored in the columns.

    """
    import oxyba as ox
    import numpy as np
    import warnings

    # shuffle K blocks from the N row indicies
    if idxmat is None:
        if K is None:
            raise Exception('Number of blocks K>1 is required')
        N = data.shape[0]  # number of observations
        idxmat, _ = ox.block_idxmat_shuffle(N, K, random_state)
    else:
        K = idxmat.shape[1]

    # display warnings
    if K < 30:
        warnings.warn((
            "The number of blocks is K<30 and will supply an "
            "insufficient number of for t-Test (model comparision) "
            "in oxyba.crossvalidation_stats! K=40 is suggested."))
    if int(idxmat.shape[0]) < 30:
        warnings.warn((
            "The blocksize is int(N/K)<30 and the fitness score of "
            "the validation blocks might be insufficient."))

    # declare lists
    errors = []
    coeffs = []

    # loop over all blocks
    for b in range(K):
        # temporary store indicies when using block b for validation
        idx_train, idx_valid = ox.block_idxmat_sets(idxmat, b)

        # estimate with all blocks that are not block b
        c = fitfunc(data[idx_train, :])
        coeffs.append(c)

        # compute error of validation block
        e = evalfunc(data[idx_valid, :], c)
        errors.append(e)

    # done
    return np.array(errors), np.array(coeffs), idxmat
