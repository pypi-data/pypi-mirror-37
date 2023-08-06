
def clean_german_date(x):
    """Convert a string with a German date 'DD.MM.YYYY' to Datetime objects

    Parameters
    ----------
    x : str, list, tuple, numpy.ndarray, pandas.DataFrame
        A string with a German formated date,
        or an array of these strings, e.g. list, ndarray, df.

    Returns
    -------
    y : str, list, tuple, numpy.ndarray, pandas.DataFrame
        A datetime object or array of datetime objects.

    Example
    -------
    The function aims to convert a string as follows

        '23.09.2012'  => datetime(2012, 9, 23, 0, 0)

    Code Example
    ------------
        print(clean_german_date('23.09.2012'))

    Behavior
    --------
    - If it is not a string with date format 'DD.MM.YYYY' then None is returned

    """
    import numpy as np
    import pandas as pd
    from datetime import datetime

    def proc_elem(e):
        try:
            return datetime.strptime(e, '%d.%m.%Y')
        except Exception as e:
            print(e)
            return None

    def proc_list(x):
        return [proc_elem(e) for e in x]

    def proc_ndarray(x):
        tmp = proc_list(list(x.reshape((x.size,))))
        return np.array(tmp).reshape(x.shape)

    # transform string, list/tuple, numpy array, pandas dataframe
    if isinstance(x, str):
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
