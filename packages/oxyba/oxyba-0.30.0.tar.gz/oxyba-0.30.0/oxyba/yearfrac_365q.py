
def yearfrac_365q(d1, d2):
    """date difference "d1-d2" as year fractional"""

    # import modules
    from datetime import date
    from oxyba import date_to_datetime

    # define yearfrac formula
    # toyf = lambda a,b: (a - b).days / 365.2425
    def toyf(a, b):
        a = date_to_datetime(a) if isinstance(a, date) else a
        b = date_to_datetime(b) if isinstance(b, date) else b
        return (a - b).days / 365.2425

    # deal with scalars and vectors
    n1 = len(d1) if hasattr(d1, "__iter__") else 1
    n2 = len(d2) if hasattr(d2, "__iter__") else 1

    # compute yearfrac
    if n1 == 1 and n2 == 1:
        return toyf(d1, d2)
    elif n1 > 1 and n2 == 1:
        return [toyf(elem, d2) for elem in d1]
    elif n1 == 1 and n2 > 1:
        return [toyf(d1, elem) for elem in d2]
    elif n1 > 1 and n1 == n2:
        return [toyf(e1, e2) for e1, e2 in zip(d1, d2)]
    else:
        raise Exception("d1 and d2 have the wrong dimensions.")
