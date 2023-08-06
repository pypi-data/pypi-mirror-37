
def clean_add_strdec(*args, prec=28):
    """add two columns that contain numbers as strings"""

    # load modules
    import pandas as pd
    import numpy as np
    import re
    from decimal import Decimal, getcontext
    getcontext().prec = prec

    # initialize result as 0.0
    def proc_elem(*args):
        t = Decimal('0.0')
        for a in args:
            if isinstance(a, str):
                a = re.sub('[^0-9\.\-]+', '', a)

            if a and pd.notnull(a):
                t += Decimal(a)

        return str(t)

    def proc_list(arr):
        return [proc_elem(*row) for row in arr]

    def proc_ndarray(arr):
        return np.array(proc_list(arr))

    # transform depending on provided datatypes
    if isinstance(args[0], (list, tuple)):
        return proc_list(args[0])
    elif isinstance(args[0], np.ndarray):
        return proc_ndarray(args[0])
    elif isinstance(args[0], pd.DataFrame):
        return pd.DataFrame(proc_ndarray(args[0].values),
                            index=args[0].index)
    else:
        return proc_elem(*args)
