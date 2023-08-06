
def mapencode(data, mapping, nastate=False):
    import grouplabelencode
    import warnings

    warnings.warn(
        ("'oxyba.mapencode' is deprecated;"
         "use 'grouplabelencode.grouplabelencode' instead."),
        DeprecationWarning, stacklevel=2)

    return grouplabelencode.grouplabelencode(data, mapping, nastate=nastate)
