
def linreg_ols_pinv(y, X, rcond=1e-15):
    """Linear Regression, OLS, by multiplying with Pseudoinverse"""
    import numpy as np
    try:  # multiply with inverse to compute coefficients
        return np.dot(np.linalg.pinv(
            np.dot(X.T, X), rcond=rcond), np.dot(X.T, y))
    except np.linalg.LinAlgError:
        print("LinAlgError: SVD does not converge")
        return None
