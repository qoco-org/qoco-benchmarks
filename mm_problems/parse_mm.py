import cvxpy as cp
import numpy as np
import scipy as sp

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
    n = len(mm_data["lb"])
    Q = mm_data["Q"]
    Amm = mm_data["A"]
    c = np.squeeze(mm_data["c"], axis=1)
    rl = np.squeeze(mm_data["rl"], axis=1)
    ru = np.squeeze(mm_data["ru"], axis=1)
    lb = np.squeeze(mm_data["lb"], axis=1)
    ub = np.squeeze(mm_data["ub"], axis=1)

    P = Q

    eq_idx = np.where(ru == rl)[0]
    bnd_idx = np.where(ru != rl)[0]

    # Parse out equality constraints.
    b = ru[eq_idx]
    A = Amm[eq_idx, :]
    Amm = Amm[bnd_idx, :]
    ru = ru[bnd_idx]
    rl = rl[bnd_idx]

    # Parse lower bound to remove +inf.
    Glb = -np.eye(n)
    idx = np.where(lb != -np.inf)
    Glb = Glb[idx]
    hlb = lb[idx]

    # Parse upper bound to remove +inf.
    Gub = np.eye(n)
    idx = np.where(ub != np.inf)
    Gub = Gub[idx]
    hub = ub[idx]

    # Parse inequality constraints to remove (+/-) inf
    idx = np.where(rl != -np.inf)
    Grl = Amm[idx]
    hrl = rl[idx]

    idx = np.where(ru != np.inf)
    Gru = Amm[idx]
    hru = ru[idx]

    G = sp.sparse.vstack(
        (sp.sparse.csc_matrix(Glb), sp.sparse.csc_matrix(Gub), Grl, Gru)
    )
    h = np.hstack((hlb, hub, hrl, hru))

    p = A.shape[0]
    m = G.shape[0]
    l = m
    nsoc = 0
    q = []

    G = G if m > 0 else None
    h = h if m > 0 else None
    A = A if p > 0 else None
    b = b if p > 0 else None

    return n, m, p, P, c, A, b, G, h, l, nsoc, q


# TODO: Eliminate +/- inf from l and u
def parse_mm_osqp(mm_data):
    n = len(mm_data["lb"])
    P = mm_data["Q"]
    q = np.squeeze(mm_data["c"], axis=1)

    Amm = mm_data["A"]
    rl = np.squeeze(mm_data["rl"], axis=1)
    ru = np.squeeze(mm_data["ru"], axis=1)
    lb = np.squeeze(mm_data["lb"], axis=1)
    ub = np.squeeze(mm_data["ub"], axis=1)

    A = sp.sparse.vstack((sp.sparse.eye(n), Amm))
    l = np.hstack((lb, rl))
    u = np.hstack((ub, ru))

    return P, q, A, l, u
