
def subjcorr_luriegold(R):
    import luriegold
    import warnings

    warnings.warn(
        ("'oxyba.subjcorr_onepara' is deprecated;"
         "use 'onepara.onpara' instead."),
        DeprecationWarning, stacklevel=2)

    return luriegold.luriegold(R)
