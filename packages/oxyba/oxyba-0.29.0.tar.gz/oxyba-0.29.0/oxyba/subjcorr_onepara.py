
def subjcorr_onepara(R):
    import onepara
    import warnings

    warnings.warn(
        ("'oxyba.subjcorr_onepara' is deprecated;"
         "use 'onepara.onpara' instead."),
        DeprecationWarning, stacklevel=2)

    return onepara.onepara(R)
