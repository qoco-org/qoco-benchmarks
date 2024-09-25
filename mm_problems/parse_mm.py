import cvxpy as cp
import numpy as np
import scipy as sp
import clarabel

# Parses QP from Maros-Meszaros standard form to QCOS standard form
#
# Maros-Meszaros standard form
#   minimize    (1/2) x'Qx + c'x
#   subject to  rl <= Ax <= ru
#               lb <=  x <= ub
#
# QCOS standard form
# minimize   (1/2)x'Px + c'x
# subject to Ax = b
#            Gx <= h
#
# OSQP standard form
# minimize   (1/2)x'Px + q'x
# subject to l <= Ax <= u
#


def parse_mm_qcos(mm_data):
    P, c, A, l, u = parse_mm_osqp(mm_data)

    eq_idx = np.where(l == u)[0]
    ineq_idx = np.where(l != u)[0]

    Aeq = A[eq_idx]
    beq = l[eq_idx]

    Aineq = A[ineq_idx]
    uineq = u[ineq_idx]
    lineq = l[ineq_idx]

    Aineq = sp.sparse.vstack((Aineq, -Aineq))
    bineq = np.hstack((uineq, -lineq))

    # Drop inf
    idx = np.where(bineq != np.inf)
    Aineq = Aineq[idx]
    bineq = bineq[idx]

    p = Aeq.shape[0]
    m = Aineq.shape[0]
    n = Aeq.shape[1]

    l = m
    nsoc = 0
    q = []

    return n, m, p, P, c, Aeq, beq, Aineq, bineq, l, nsoc, q


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

    P, q, A, l, u = parse_mm_osqp(mm_data)

    eq_idx = np.where(l == u)[0]
    ineq_idx = np.where(l != u)[0]

    Aeq = A[eq_idx]
    beq = l[eq_idx]

    Aineq = A[ineq_idx]
    uineq = u[ineq_idx]
    lineq = l[ineq_idx]

    Aineq = sp.sparse.vstack((Aineq, -Aineq))
    bineq = np.hstack((uineq, -lineq))

    # Drop inf
    idx = np.where(bineq != np.inf)
    Aineq = Aineq[idx]
    bineq = bineq[idx]

    p = Aeq.shape[0]
    m = Aineq.shape[0]

    A = sp.sparse.vstack((Aeq, Aineq))
    b = np.hstack((beq, bineq))

    cones = [clarabel.ZeroConeT(p), clarabel.NonnegativeConeT(m)]

    return P, q, A, b, cones


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
