
def linreg_ols_qr(y, X):
    """Linear Regression, OLS, inverse by QR Factoring"""
    import numpy as np
    try:  # multiply with inverse to compute coefficients
        q, r = np.linalg.qr(np.dot(X.T, X))
        return np.dot(np.dot(np.linalg.inv(r), q.T), np.dot(X.T, y))
    except np.linalg.LinAlgError:
        print("LinAlgError: Factoring failed")
        return None
