import scipy.io
from pathlib import Path
import pandas as pd
from mm_problems.mm_opt import *
import cvxpy as cp
from solvers.solvers import *
from utils import parse_maros


high_acc = 1e-7
low_acc = 1e-5

solve_dict_qoco = {}
solve_dict_clarabel = {}
solve_dict_gurobi = {}
solve_dict_mosek = {}
solve_dict_ecos = {}
directory = Path("mm_problems/MAT_Files")
for file_path in directory.iterdir():
    if file_path.is_file():
        mat = scipy.io.loadmat(file_path)
        problem_name = file_path.stem
        # print(file_path)
        if len(mat["lb"]) > 5000:
            continue

        list = [
            "QSHIP08S",
            "QSHIP04L",
            "QSHIP04S",
            "QSC205",
            "QFORPLAN",
            "QPCBOEI1",
            "QPILOTNO",
            "QSIERRA",
            "QSHIP08L",
            "QSHIP12S",
            "QPCBOEI2",
            "YAO",
            "QGFRDXPN",
            "QBRANDY",
        ]
        # if problem_name not in list:
        #     continue

        # Set up CVXPY problem.
        n, m, p, P, c, A, b, G, h, l, nsoc, q = parse_maros(mat)
        x = cp.Variable(n)
        obj = cp.Minimize(0.5 * cp.quad_form(x, P, True) + c.T @ x)
        con = []
        if p > 0:
            con += [A @ x == b]
        if m > 0:
            con += [G @ x <= h]
        prob = cp.Problem(obj, con)

        # QOCO
        solve_dict_qoco[problem_name] = qoco_solve(prob, 1e-7, N=1)

        # Gurobi
        # solve_dict_gurobi[problem_name] = gurobi_solve(prob, 1e-7, N=1)

        # # Mosek
        # solve_dict_mosek[problem_name] = mosek_solve(prob, 1e-7, N=1)

        # ## ECOS
        # solve_dict_ecos[problem_name] = ecos_solve(prob, 1e-7, N=1)

        # # Clarabel
        # solve_dict_clarabel[problem_name] = clarabel_solve(prob, 1e-7, N=1)

df_qoco = pd.DataFrame(solve_dict_qoco).T
df_clarabel = pd.DataFrame(solve_dict_clarabel).T
df_gurobi = pd.DataFrame(solve_dict_gurobi).T
df_mosek = pd.DataFrame(solve_dict_mosek).T
df_ecos = pd.DataFrame(solve_dict_ecos).T

df_qoco.to_csv("results/maros/qoco.csv")
# df_clarabel.to_csv("results/maros/clarabel.csv")
# df_gurobi.to_csv("results/maros/gurobi.csv")
# df_mosek.to_csv("results/maros/mosek.csv")
# df_ecos.to_csv("results/maros/ecos.csv")
