
def clean_dateobject_to_string(x):
    """Convert a Pandas Timestamp object or datetime object
    to 'YYYY-MM-DD' string

    Parameters
    ----------
    x : str, list, tuple, numpy.ndarray, pandas.DataFrame
        A Pandas Timestamp object or datetime object,
        or an array of these objects

    Returns
    -------
    y : str, list, tuple, numpy.ndarray, pandas.DataFrame
        A string 'YYYY-MM-DD' or array of date strings.

    Example
    -------
    The function aims to convert a string as follows

        Timestamp('2014-09-23 00:00:00') => '2014-09-23'
        datetime.datetime(2014,9,23,0,0) => '2014-09-23'

    Code Example
    ------------
        print(clean_dateobject_to_string(pd.Timestamp('2014-09-23 00:00:00')))
        '2014-09-23'

        print(clean_dateobject_to_string(datetime(2014,9,23,0,0)))
        '2014-09-23'

    Behavior
    --------
    - If it is not an object with strftime function the None is return

    """
    import numpy as np
    import pandas as pd

    def proc_elem(e):
        try:
            return e.strftime("%Y-%m-%d")
        except Exception as e:
            print(e)
            return None

    def proc_list(x):
        return [proc_elem(e) for e in x]

    def proc_ndarray(x):
        tmp = proc_list(list(x.reshape((x.size,))))
        return np.array(tmp).reshape(x.shape)

    # transform string, list/tuple, numpy array, pandas dataframe
    if "strftime" in dir(x):
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
