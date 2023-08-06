
def crossvalidation_stats(errors1, errors2):
    """Paired difference test
    of the CV errors of two models

    Parameters:
    -----------
    errors1 : ndarray
        The CV errors model 1

    errors2 : ndarray
        The CV errors model 2

    Returns:
    --------
    pvalue : float
        Two-sided P-value if the differences between err1 and err2
        are significant

    tscore : float
        t-statistics

    se : float
        Standard Error of the CV-Error-Difference

    mu : float
        The average difference between err1 and err2

    """
    # load modules
    import numpy as np
    import scipy.stats
    import warnings

    # Number of blocks
    K = errors1.shape[0]

    # display warnings
    if K < 30:
        warnings.warn((
            "The number of blocks is K<30 what is insufficient "
            "for conducting a t-Test to compare both models! "
            "K=40 is suggested."))

    # difference between errors
    delta = errors1 - errors2

    # the average difference
    mu = np.mean(delta)

    # Standard Error of the CV-Error-Difference
    #   se = np.sqrt(np.sum((delta-np.mean(delta))**2)/K)
    se = np.std(delta)

    # t-statistics
    tscore = mu / se

    # Two-sided P-value
    pvalue = scipy.stats.t.sf(np.abs(tscore), K - 1) * 2

    # done
    return pvalue, tscore, se, mu


def crossvalidation_error(errors):
    """Crossvalidation Errors"""
    import numpy as np
    return np.mean(errors), np.std(errors)
