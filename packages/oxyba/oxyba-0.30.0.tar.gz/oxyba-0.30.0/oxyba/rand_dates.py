
def rand_dates(num, posix_start=0, posix_end=None):
    import randdate
    import warnings

    warnings.warn(
        ("'oxyba.rand_dates' is deprecated;"
         "use 'randdate.randdate' instead."),
        DeprecationWarning, stacklevel=2)

    return randdate.randdate(
        num, posix_start=posix_start, posix_end=posix_end)
