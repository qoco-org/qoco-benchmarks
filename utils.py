import numpy as np
import scipy as sp
import os, shutil


def get_average_solvetime(df):
    size = set(df["size"])
    size = [*size]
    size.sort()
    time = []
    for sz in size:
        idx = df[df["size"] == sz].index
        time.append(np.nanmean(df["run_time"][idx]))
    return size, time


def export_figures():
    source_dir = "./plots/"
    for file_name in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file_name)
        destination_file = os.path.join("../qoco-paper/img", file_name)

        # Check if it is a file and not a directory
        if os.path.isfile(source_file):
            shutil.copy(source_file, destination_file)


def parse_maros(mm_data):
    n = len(mm_data["lb"])
    P = mm_data["Q"]
    c = np.squeeze(mm_data["c"], axis=1)

    Amm = mm_data["A"].tocsc()
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

    G = sp.sparse.vstack((sp.sparse.identity(n), -sp.sparse.identity(n), Aineq, -Aineq)).tocsc()

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
