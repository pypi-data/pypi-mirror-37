
def isordinal(x):
    """Checks if a list or array contains ordinal data.

    Warning:
    --------
    This is not a reliable check for a variable being
    ordinal.

    The following criteria are used

    - There are more observations than unique values.
        Why? Ordinal means discrete or countable and
        I just assume that an ordinal sample should
        have some recurring (countable) values.
    - Values are integers or strings.
        Why? Ordinal scale data are usually labels
        (e.g. strings) or are encoded labels (e.g.
        as integers).
    - Ordinal scale data is sortable
        Integers imply that the Analyst encoded the
        labels according to the ordinal data's "natural
        order". Strings would imply that the alphabetic
        order would be the natual order (what is usually
        not the case)

    Usage:
    ------
        obs = 10
        np.random.seed(42)
        x1 = np.random.randint(1,50, (obs,))
        x2 = np.random.randint(0,3, (obs,))
        x3 = np.random.uniform(0,3, (obs,))

        flag, msg = isordinal(x1)
        if not flag:
            warnings.warn(msg)
    """
    import numpy as np

    if len(x) == len(np.unique(x)):
        return False, ("number of observations equals the "
                       "number of unique values.")

    if not isinstance(x[0], str):
        if not np.all(np.equal(np.mod(x, 1), 0)):
            return False, "elements are not integer or strings."

    return True, "is ordinal"
