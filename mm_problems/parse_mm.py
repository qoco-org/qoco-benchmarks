import cvxpy as cp
import numpy as np
import scipy as sp
import clarabel

# Parses QP from Maros-Meszaros standard form to QOCO standard form
#
# Maros-Meszaros standard form
#   minimize    (1/2) x'Qx + c'x
#   subject to  rl <= Ax <= ru
#               lb <=  x <= ub
#
# QOCO standard form
# minimize   (1/2)x'Px + c'x
# subject to Ax = b
#            Gx <= h
#
# OSQP standard form
# minimize   (1/2)x'Px + q'x
# subject to l <= Ax <= u
#


def parse_mm_qoco(mm_data):
    n = len(mm_data["lb"])
    P = mm_data["Q"]
    c = np.squeeze(mm_data["c"], axis=1)

    Amm = mm_data["A"]
    rl = np.squeeze(mm_data["rl"], axis=1)
    ru = np.squeeze(mm_data["ru"], axis=1)
    lb = np.squeeze(mm_data["lb"], axis=1)
    ub = np.squeeze(mm_data["ub"], axis=1)

    eq_idx = np.where(rl == ru)[0]
    ineq_idx = np.where(rl != ru)[0]

    Aeq = Amm[eq_idx]
    beq = rl[eq_idx]

    Aineq = Amm[ineq_idx]
    uineq = ru[ineq_idx]
    lineq = rl[ineq_idx]

    G = sp.sparse.vstack((np.eye(n), -np.eye(n), Aineq, -Aineq)).tocsc()
    h = np.hstack((ub, -lb, uineq, -lineq))

    # Drop inf
    idx = np.where(h != np.inf)
    G = G[idx]
    h = h[idx]

    m = G.shape[0]
    p = Aeq.shape[0]

    l = m
    nsoc = 0
    q = []

    return n, m, p, P, c, Aeq, beq, G, h, l, nsoc, q


def parse_mm_osqp(mm_data):
    n = len(mm_data["lb"])
    P = mm_data["Q"]
    q = np.squeeze(mm_data["c"], axis=1)

    Amm = mm_data["A"]
    rl = np.squeeze(mm_data["rl"], axis=1)
    ru = np.squeeze(mm_data["ru"], axis=1)
    lb = np.squeeze(mm_data["lb"], axis=1)
    ub = np.squeeze(mm_data["ub"], axis=1)

    A = sp.sparse.vstack((sp.sparse.eye(n), Amm)).tocsc()
    l = np.hstack((lb, rl))
    u = np.hstack((ub, ru))

    idx = np.where((l != -np.inf) & (u != np.inf))

    A = A[idx]
    l = l[idx]
    u = u[idx]

    return P, q, A, l, u


def parse_mm_clarabel(mm_data):

    n = len(mm_data["lb"])
    P = mm_data["Q"]
    c = np.squeeze(mm_data["c"], axis=1)

    Amm = mm_data["A"]
    rl = np.squeeze(mm_data["rl"], axis=1)
    ru = np.squeeze(mm_data["ru"], axis=1)
    lb = np.squeeze(mm_data["lb"], axis=1)
    ub = np.squeeze(mm_data["ub"], axis=1)

    eq_idx = np.where(rl == ru)[0]
    ineq_idx = np.where(rl != ru)[0]

    Aeq = Amm[eq_idx]
    beq = rl[eq_idx]

    p = Aeq.shape[0]

    Aineq = Amm[ineq_idx]
    uineq = ru[ineq_idx]
    lineq = rl[ineq_idx]

    G = sp.sparse.vstack((np.eye(n), -np.eye(n), Aineq, -Aineq)).tocsc()
    h = np.hstack((ub, -lb, uineq, -lineq))

    # Drop inf
    idx = np.where(h != np.inf)
    G = G[idx]
    h = h[idx]
    m = G.shape[0]

    A = sp.sparse.vstack((Aeq, G))
    b = np.hstack((beq, h))

    cones = [clarabel.ZeroConeT(p), clarabel.NonnegativeConeT(m)]
    return P, c, A, b, p, m, cones


def parse_mm_piqp(mm_data):

    n = len(mm_data["lb"])
    P = mm_data["Q"]
    c = np.squeeze(mm_data["c"], axis=1)

    Amm = mm_data["A"]
    rl = np.squeeze(mm_data["rl"], axis=1)
    ru = np.squeeze(mm_data["ru"], axis=1)
    x_lb = np.squeeze(mm_data["lb"], axis=1)
    x_ub = np.squeeze(mm_data["ub"], axis=1)

    eq_idx = np.where(rl == ru)[0]
    ineq_idx = np.where(rl != ru)[0]

    Aeq = Amm[eq_idx]
    beq = rl[eq_idx]

    Aineq = Amm[ineq_idx]
    uineq = ru[ineq_idx]
    lineq = rl[ineq_idx]

    Aineq = sp.sparse.vstack((Aineq, -Aineq))
    bineq = np.hstack((uineq, -lineq))

    # Drop inf
    idx = np.where(bineq != np.inf)
    G = Aineq[idx]
    h = bineq[idx]

    return P, c, Aeq, beq, G, h, x_lb, x_ub
