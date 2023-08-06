
def clean_german_number(x):
    """Convert a string with a German number into a Decimal

    Parameters
    ----------
    x : str, list, tuple, numpy.ndarray, pandas.DataFrame
        A string with a number with German formatting,
        or an array of these strings, e.g. list, ndarray, df.

    Returns
    -------
    y : str, list, tuple, numpy.ndarray, pandas.DataFrame
        A string or array of strings that can be converted
        to a numeric data type (e.g. Decimal, float, int).

    Example
    -------
    The function aims to convert a string as follows

        '1.234'     => '1234'
        '1234'      => '1234'
        '1.234,56'  => '1234.56'
        '1.234.560' => '1234560'
        '+123'      => '123'
        '-123'      => '-123'

    Code Example
    ------------
        print(clean_german_number('1.234,56'))
        '1234.56'


    Behavior
    --------
    - The function will return None if the element is not a string
    - The function assumes that provided string are German numbers.
    - There will NO check if it is a regular number.
    - No conversion to a numeric data type (have to be done afterwards)

    Notes
    -----
    The command `x.dropna().apply(proc_elem)` is not working for
    pandas dataframes. Maybe the `proc_elem` sub function is too big
    or complex for pandas' apply method.

    """
    import numpy as np
    import pandas as pd
    import re

    def proc_elem(e):
        # abort if it is not a string
        if not isinstance(e, str):
            return None

        # strip all char except digits, ".", "," and "-"
        s = re.sub('[^0-9\.\,\-]+', '', e)

        # abort if nothing is left
        if len(s) is 0:
            return None

        # extra check regarding "-" modifier
        m = ""
        if s[0] is "-":
            if len(s) > 1:
                m = "-"
                s = s[1:]
            else:
                return None

        # remove the "-" from the string
        s = re.sub('[^0-9\.\,]+', '', s)

        # abort if nothing is left
        if len(s) is 0:
            return None

        # abort if the number of "," (decimal sep) is bigger than 1
        if s.count(',') > 1:
            return None

        # about if the decimal sep "," occurs before a 000' sep "."
        if s.count('.') > 0 and s.count(',') > 0:
            rev = s[::-1]
            if rev.find(",") > rev.find("."):
                return None

        # remove 000' seperators "."
        s = s.replace('.', '')

        # convert comma to dot
        s = s.replace(',', '.')

        # if just a dot is left "."
        if s == ".":
            return None

        # reattach the "-" modifier
        return m + s

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
                            columns=x.columns, index=x.index)
    else:
        return None
