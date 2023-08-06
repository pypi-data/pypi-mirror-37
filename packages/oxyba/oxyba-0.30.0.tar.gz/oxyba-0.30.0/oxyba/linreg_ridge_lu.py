
def linreg_ridge_lu(y, X, lam=0.01):
    import numpy as np
    try:
        cols = X.shape[1]
        P = np.dot(X.T, X) + lam * np.eye(cols)
        return np.linalg.solve(P, np.dot(X.T, y))
    except np.linalg.LinAlgError:
        print("LinAlgError: X*X'+lam*I is singular or not square.")
        return None
