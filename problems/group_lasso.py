import cvxpy as cp
import numpy as np
from scipy import sparse

np.random.seed(123)


def group_lasso(ngroups):

    group_size = 10
    n = ngroups * group_size
    m = 25 * n
    lam = 1

    xtrue = np.zeros(n)
    if ngroups > 1:
        for i in range(int(ngroups / 2)):
            xtrue[i * group_size : (i + 1) * group_size] = np.random.randn(group_size)
    else:
        xtrue[0:group_size] = np.random.randn(group_size)

    A = sparse.random(m, n, density=0.10, data_rvs=np.random.randn, format="csc")
    e = np.random.randn(m) / n
    b = A @ xtrue + e
    y = cp.Variable(m)
    x = cp.Variable(n)
    con = [y == A @ x - b]

    obj = cp.quad_form(y, np.eye(m))
    for i in range(ngroups):
        obj += lam * cp.norm(x[i * group_size : (i + 1) * group_size])
    prob = cp.Problem(cp.Minimize(obj), con)
    return prob
