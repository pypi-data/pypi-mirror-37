
def drop_empty_records(x, axis=1):
    """delete data items that contains only nan (or inf) """
    # load module
    import numpy as np
    # input args check
    if not isinstance(x, np.ndarray or np.matrix):
        raise ValueError("x is not a numpy.ndarray or numpy.matrix.")

    # index
    idx = np.logical_not(np.all(np.logical_or(
        np.isnan(x), np.isinf(x)), axis=axis))

    if axis is 1:
        return x[idx, :].copy()
    elif axis is 0:
        return x[:, idx].copy()
    else:
        raise ValueError("only 2-dimensional datasets are supported.")
