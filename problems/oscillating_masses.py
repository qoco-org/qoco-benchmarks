import cvxpy as cp
import scipy as sp
import numpy as np


def oscillating_masses(T):
    dt = 0.25
    n = 4

    Q = np.diag(np.random.uniform(0, 10, 2 * n))
    R = np.diag(np.random.uniform(0, 10, n))

    band = -2 * np.eye(n)
    for i in range(1, n):
        band[i, i - 1] = 1
        band[i - 1, i] = 1
    Ac = np.block([[np.zeros((n, n)), np.eye(n)], [band, np.zeros((n, n))]])
    Bc = np.block([[np.zeros((n, n))], [np.eye(n)]])

    A = sp.linalg.expm(Ac * dt)
    B = np.linalg.inv(Ac) @ (A - np.eye(2 * n)) @ Bc

    u = cp.Variable((n, T))
    x = cp.Variable((2 * n, T + 1))

    umax = 5
    xmax = 2
    xlim = xmax * np.ones(2 * n)
    ulim = umax * np.ones(n)

    x0 = np.clip(np.random.randn(2 * n), -0.90 * xlim, 0.90 * xlim)
    obj = 0
    con = [x[:, 0] == x0]
    for k in range(T):
        obj += cp.quad_form(x[:, k], Q) + cp.quad_form(u[:, k], R)
        con += [x[:, k + 1] == A @ x[:, k] + B @ u[:, k]]
        con += [-xlim <= x[:, k], x[:, k] <= xlim]
        con += [-ulim <= u[:, k], u[:, k] <= ulim]
    obj += cp.quad_form(x[:, T], Q)

    prob = cp.Problem(cp.Minimize(obj), con)
    return prob, x0, Q, R, A, B, umax, xmax
