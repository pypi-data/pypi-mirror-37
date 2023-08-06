
def subjcorr_kfactor(R, k=2, algorithm='COBYLA'):
    import kfactor
    import warnings

    warnings.warn(
        ("'oxyba.subjcorr_kfactor' is deprecated;"
         "use 'kfactor.kfactor' instead."),
        DeprecationWarning, stacklevel=2)

    return kfactor.kfactor(R, k=k, algorithm=algorithm)
