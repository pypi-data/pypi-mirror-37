
def clean_to_decimal(x, prec=28):
    """Convert an string, int or float to Decimal object

    Parameters
    ----------
    x : str, list, tuple, numpy.ndarray, pandas.DataFrame
        A string, int or float number, or a list, array or
        dataframe of these.

    digits : int
        (Default prec=None)
        Set the getcontext precision

    Returns
    -------
    y : str, list, tuple, numpy.ndarray, pandas.DataFrame
        Decimal object or array of Decimal objects

    Example
    -------
        clean_to_decimal('12.345')
            Decimal('12.345')

        clean_to_decimal('12.345', prec=2)
            Decimal('12')

        clean_to_decimal(12.345)
            Decimal('12.34500000000000063948846218')

        clean_to_decimal(12.345, prec=5)
            Decimal('12.345')

    """
    import numpy as np
    import pandas as pd
    import decimal

    def proc_elem(e):
        try:
            return decimal.Decimal(e) + decimal.Decimal('0.0')
        except Exception as e:
            print(e)
            return None

    def proc_list(x):
        return [proc_elem(e) for e in x]

    def proc_ndarray(x):
        tmp = proc_list(list(x.reshape((x.size,))))
        return np.array(tmp).reshape(x.shape)

    # set precision
    if prec:
        decimal.getcontext().prec = prec

    # transform string, list/tuple, numpy array, pandas dataframe
    if isinstance(x, (str, int, float)):
        return proc_elem(x)
    elif isinstance(x, (list, tuple)):
        return proc_list(x)
    elif isinstance(x, np.ndarray):
        return proc_ndarray(x)
    elif isinstance(x, pd.DataFrame):
        return pd.DataFrame(proc_ndarray(x.values),
                            columns=x.columns,
                            index=x.index)
    else:
        return None
