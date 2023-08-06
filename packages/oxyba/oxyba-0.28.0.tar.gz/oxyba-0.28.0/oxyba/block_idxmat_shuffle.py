def block_idxmat_shuffle(numdraws, numblocks, random_state=None):
    """Create K columns with unique random integers from 0 to N-1

    Purpose:
    --------
    - Create K blocks for k-fold cross-validation

    Parameters:
    -----------
    numdraws : int
        number of observations N or sample size N

    numblocks : int
        number of blocks K

    Example:
    --------
        import pandas as pd
        import numpy as np
        import oxyba as ox

        X = np.random.normal(size=(7,5), scale=50).round(1)
        N,_ = X.shape

        K = 3;  #number of blocks
        idxmat, dropped = ox.block_idxmat_shuffle(N,K)

        for b in range(K):
            print('\nBlock:',b)
            print(pd.DataFrame(X[idxmat[:,b],:], index=idxmat[:,b]))

        print('\nDropped observations\n', X[dropped,:] )
        print('\nrow indicies of dropped observations:', dropped, '\')

    Why is this useful?
    -------------------
    - Avoid creating copies of dataset X during run time
    - Shuffle the indicies of a data point rather than the
        data points themselve

    Links:
    ------
    - How numpy's permutation works, https://stackoverflow.com/a/15474335
    """
    # load modules
    import numpy as np

    # minimum block size: bz=int(N/K)
    blocksize = int(numdraws / numblocks)

    # shuffle vector indicies: from 0 to N-1
    if random_state:
        np.random.seed(random_state)
    obsidx = np.random.permutation(numdraws)

    # how many to drop? i.e. "numdrop = N - bz*K"
    numdrop = numdraws % numblocks
    dropped = obsidx[:numdrop]
    obsidx = obsidx[numdrop:]

    # reshape the remaing vector indicies into a matrix
    idxmat = obsidx.reshape((blocksize, numblocks))

    # output the indicies for the blocks, and indicies of dropped obserations
    return idxmat, dropped
