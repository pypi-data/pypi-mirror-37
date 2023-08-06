import numpy as np
import scipy.optimize
import warnings


def kfactor(R, k=2, algorithm='COBYLA'):
    """k-Factor Nearest Correlation Matrix Fit

    Parameters:
    -----------
    R : ndarray
        an illconditioned <d x d> correlation matrix,
        e.g. oxyba.illcond_corrmat

    k : int
        Number of factors (Default: 2)

    algorithm : str
        'COBYLA' (Default) or 'SLSQP'.
        Use 'COBYLA' because it is faster and more
        likely to converge to a feasible solution.

    Returns:
    --------
    C : ndarray
        Fitted <d x d> Correlation Matrix.

    flag : bool
        True if C is a feasible solution
        or False if C is ill-conditioned

    X : ndarray
        The <d x k> Factor-Matrix.

    results : scipy.optimize.optimize.OptimizeResult
        Scipy's result object.

    Links
    -----
    * Higham, N.J., 2002. Computing the nearest correlation
        matrix -- a problem from finance. IMA Journal of
        Numerical Analysis 22, 329–343.
        https://doi.org/10.1093/imanum/22.3.329
        http://www.maths.manchester.ac.uk/~higham/narep/narep369.pdf

    * Higham, Nick, 2009, presentation
        https://www.nag.com/market/nagquantday2009_ComputingaNearestCorrelationMatrixNickHigham.pdf
    """

    # subfunctions
    def corradjusteigen(C):
        """Reset negative diagonal elements 'D' to +1e-308
            This trick ensures that C semipositive definite.
        """
        D, V = np.linalg.eig(C)
        Dadj = np.diag(np.maximum(1e-308, D))
        Cadj = np.dot(np.dot(V, Dadj), V.T)
        Cadj = (Cadj + Cadj.T) / 2.
        return Cadj

    def xtocorr(x, d, k):
        """Convert vector 'x' into <d x k> matrix 'X'
           and compute the Correlation Matrix
        """
        X = x.reshape(d, k)
        xx = np.dot(X, X.T)
        C = np.diag(np.diag(1 - xx)) + xx
        Cadj = corradjusteigen(C)
        return Cadj, X

    def objectivefunc(x, R, d, k):
        """Objective Function of the Minimization Probem.
            The Sum of Squared Diff (SSR) between the
            ill-conditioned matrix 'R' and the current
            iteration of 'C'
        """
        C, _ = xtocorr(x, d, k)
        f = np.sum((R - C)**2)
        extra = 2 * d * np.sum(np.abs(np.diag(C) - 1.0))
        return f + extra

    def gradientfunc(x, R, d, k):
        X = np.matrix(x.reshape(d, k))
        G = 4 * (X * (X.T * X) - R * X + X - np.diag(np.diag(X * X.T)) * X)
        return np.array(G.reshape(G.size,))

    def nlcon_ineq(x, d, k):
        """Non-Linear Constraint
            The sum of the d absolute parameter values
            for each of the k factors have to be less than 1.
            (Sum for each of the k columns is lt 1)
        """
        X = x.reshape(d, k)
        return np.sum(X**2, axis=1) - 1

    # check k
    if k < 2:
        raise Exception('k<2 is not supported')

    # check eligible algorithm
    if algorithm not in ('COBYLA', 'SLSQP'):
        raise Exception('Optimization Algorithm not supported.')

    # dimension of the correlation matrix
    d = R.shape[0]

    # start values of the optimization are Ones
    x0 = np.ones(shape=(d * k, ))

    # simple lower (-1) and upper (+1) bounds
    bnds = [(-1, +1) for _ in range(d * k)]

    # for each of the k factors, the sum of its d absolute params
    # values has to be less than 1
    con_ineq = {'type': 'ineq', 'args': (d, k), 'fun': nlcon_ineq}

    # set maxiter
    if algorithm is 'SLSQP':
        opt = {'ftol': 1e-12, 'maxiter': d * k * 1000, 'disp': False}
    else:
        opt = {'tol': 1e-8, 'catol': 2e-4, 'maxiter': d * k * 200,
               'disp': False}

    # run the optimization
    results = scipy.optimize.minimize(
        objectivefunc, x0,
        jac=gradientfunc,
        args=(R, d, k),
        bounds=bnds,
        constraints=[con_ineq],
        method=algorithm, options=opt)

    # convert the d*k paramter (of k factors) into the correlation matrix
    C, X = xtocorr(results.x, d, k)

    # for information purposes
    f = objectivefunc(results.x, R, d, k)
    g = gradientfunc(results.x, R, d, k)

    # check solution
    if np.any(np.linalg.eigvals(C) < 0.0):
        warnings.warn("Matrix is not positive definite")

    # done
    return C, X, f, g, results
