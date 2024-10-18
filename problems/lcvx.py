import cvxpy as cp
import numpy as np

np.random.seed(123)
def lcvx(T):
    tspan = 20
    dt = tspan / (T - 1)
    x0 = np.array([np.random.uniform(-10,10), np.random.uniform(-10,10), np.random.uniform(200,400), 0.0, 0.0, 0.0])
    # x0 = np.array([10.0, 10.0, 300.0, 0.0, 0.0, 0.0])
    g = 9.807
    tvc_max = np.deg2rad(45.0)
    rho1 = 100.0
    rho2 = 500.0
    m_dry = 25.0
    m_fuel = 10.0
    Isp = 100.0

    g0 = 9.807
    m0 = m_dry + m_fuel
    a = 1 / (Isp * g0)
    nx = 6
    nu = 3

    A = np.array(
        [
            [1.0, 0.0, 0.0, dt, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, dt, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, dt],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        ]
    )
    B = np.array(
        [
            [0.5 * dt**2, 0.0, 0.0],
            [0.0, 0.5 * dt**2, 0.0],
            [0.0, 0.0, 0.5 * dt**2],
            [dt, 0.0, 0.0],
            [0.0, dt, 0.0],
            [0.0, 0.0, dt],
        ]
    )
    G = np.array([0.0, 0.0, -0.5 * g * dt**2, 0.0, 0.0, -g * dt])
    xT = np.zeros((nx))

    x = cp.Variable((nx, T + 1))
    z = cp.Variable(T + 1)
    u = cp.Variable((nu, T + 1))
    s = cp.Variable(T + 1)

    # Objective
    obj = -z[T]

    # IC and TC
    con = [x[:, 0] == x0]
    con += [x[:, T] == xT]
    con += [z[0] == np.log(m0)]
    con += [z[T] >= np.log(m_dry)]

    # Dynamics
    for k in range(T):
        con += [x[:, k + 1] == A @ x[:, k] + B @ u[:, k] + G]
        con += [z[k + 1] == z[k] - a * s[k] * dt]

    # State and Input Constraints
    for k in range(T + 1):
        z0 = np.log(m0 - (a * rho2 * k * dt))
        mu1 = rho1 * np.exp(-z0)
        mu2 = rho2 * np.exp(-z0)
        con += [cp.norm(u[:, k]) <= s[k]]
        con += [mu1 * (1.0 - (z[k] - z0) + 0.5 * (z[k] - z0) ** 2) <= s[k]]
        con += [s[k] <= mu2 * (1.0 - (z[k] - z0))]
        con += [np.log(m0 - a * rho2 * k * dt) <= z[k]]
        con += [z[k] <= np.log(m0 - a * rho1 * k * dt)]
        con += [u[2, k] >= cp.norm(u[:, k]) * np.cos(tvc_max)]

    prob = cp.Problem(cp.Minimize(obj), con)
    return prob
