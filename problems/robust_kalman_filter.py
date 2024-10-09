import numpy as np
import cvxpy as cp


# Problem from https://www.cvxpy.org/examples/applications/robust_kalman.html
def robust_kalman_filter(n):
    T = 50
    ts, delt = np.linspace(0, T, n, endpoint=True, retstep=True)
    gamma = 0.05  # damping, 0 is no damping

    A = np.zeros((4, 4))
    B = np.zeros((4, 2))
    C = np.zeros((2, 4))

    A[0, 0] = 1
    A[1, 1] = 1
    A[0, 2] = (1 - gamma * delt / 2) * delt
    A[1, 3] = (1 - gamma * delt / 2) * delt
    A[2, 2] = 1 - gamma * delt
    A[3, 3] = 1 - gamma * delt

    B[0, 0] = delt**2 / 2
    B[1, 1] = delt**2 / 2
    B[2, 0] = delt
    B[3, 1] = delt

    C[0, 0] = 1
    C[1, 1] = 1

    sigma = 20
    p = 0.20
    np.random.seed(6)

    x = np.zeros((4, n + 1))
    x[:, 0] = [0, 0, 0, 0]
    y = np.zeros((2, n))

    # generate random input and noise vectors
    w = np.random.randn(2, n)
    v = np.random.randn(2, n)

    # add outliers to v
    np.random.seed(0)
    inds = np.random.rand(n) <= p
    v[:, inds] = sigma * np.random.randn(2, n)[:, inds]

    # simulate the system forward in time
    for t in range(n):
        y[:, t] = C.dot(x[:, t]) + v[:, t]
        x[:, t + 1] = A.dot(x[:, t]) + B.dot(w[:, t])

    x = cp.Variable(shape=(4, n + 1))
    w = cp.Variable(shape=(2, n))
    v = cp.Variable(shape=(2, n))

    tau = 2
    rho = 2

    obj = cp.sum_squares(w)
    obj += cp.sum([tau * cp.huber(cp.norm(v[:, t]), rho) for t in range(n)])
    obj = cp.Minimize(obj)

    constr = []
    for t in range(n):
        constr += [
            x[:, t + 1] == A @ x[:, t] + B @ w[:, t],
            y[:, t] == C @ x[:, t] + v[:, t],
        ]

    prob = cp.Problem(obj, constr)
    return prob
