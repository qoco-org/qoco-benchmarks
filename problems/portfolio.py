import numpy as np
import cvxpy as cp
from scipy import sparse


def portfolio(k):

    n = 100 * k
    F = sparse.random(n, k, density=0.5, data_rvs=np.random.randn, format="csc")
    D = sparse.diags(np.random.rand(n) * np.sqrt(k), format="csc")
    mu = np.random.randn(n)

    gamma = 1

    x = cp.Variable(n)
    y = cp.Variable(k)

    obj = cp.Minimize(
        cp.quad_form(x, D) + cp.quad_form(y, sparse.eye(k)) - (1 / gamma) * (mu.T @ x)
    )
    con = [cp.sum(x) == 1, F.T @ x == y, 0 <= x]
    prob = cp.Problem(obj, con)
    return prob
