

def illcond_corrmat(D, random_state=None):
    import illmat
    import warnings

    warnings.warn(
        ("'oxyba.illcond_corrmat' is deprecated;"
         "use 'illmat.illmat' instead."),
        DeprecationWarning, stacklevel=2)

    return illmat.illmat(D, random_state=random_state)
