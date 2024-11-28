import scipy.io
from pathlib import Path
import qoco
import clarabel
from mm_problems.parse_mm import *
import pandas as pd
from mm_problems.mm_opt import *
import cvxpy as cp
from solvers.solvers import *


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
        print(file_path)
        if len(mat["lb"]) > 5000:
            continue

        # QOCO
        n, m, p, P, c, A, b, G, h, l, nsoc, q = parse_mm_qoco(mat)
        G = G if m > 0 else None
        h = h if m > 0 else None
        A = A if p > 0 else None
        b = b if p > 0 else None
        prob_qoco = qoco.QOCO()
        prob_qoco.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q)
        res_qoco = prob_qoco.solve()
        solve_dict_qoco[problem_name] = {
            "status": res_qoco.status,
            "setup_time": res_qoco.setup_time_sec,
            "solve_time": res_qoco.solve_time_sec,
            "run_time": res_qoco.setup_time_sec + res_qoco.solve_time_sec,
            "obj": res_qoco.obj,
        }

        # Gurobi
        x = cp.Variable(n)
        obj = cp.Minimize(0.5 * cp.quad_form(x, P, True) + c.T @ x)
        con = []
        if A is not None:
            con += [A @ x == b]
        if G is not None:
            con += [G @ x <= h]
        prob = cp.Problem(obj, con)
        solve_dict_gurobi[problem_name] = gurobi_solve(prob, 1e-7, N=1)

        # Mosek
        solve_dict_mosek[problem_name] = mosek_solve(prob, 1e-7, N=1)

        ## ECOS
        solve_dict_ecos[problem_name] = ecos_solve(prob, 1e-7, N=1)

        # Clarabel
        P, c, A, b, p, m, cones = parse_mm_clarabel(mat)
        settings = clarabel.DefaultSettings()
        settings.tol_gap_abs = high_acc
        settings.tol_gap_rel = high_acc
        settings.tol_feas = high_acc
        settings.verbose = False
        solver = clarabel.DefaultSolver(P, c, A, b, cones, settings)
        res_clarabel = solver.solve()
        solve_dict_clarabel[problem_name] = {
            "status": str(res_clarabel.status),
            "setup_time": np.nan,
            "solve_time": res_clarabel.solve_time,
            "run_time": res_clarabel.solve_time,
            "obj": res_clarabel.obj_val,
        }

df_qoco = pd.DataFrame(solve_dict_qoco).T
df_clarabel = pd.DataFrame(solve_dict_clarabel).T
df_gurobi = pd.DataFrame(solve_dict_gurobi).T
df_mosek = pd.DataFrame(solve_dict_mosek).T
df_ecos = pd.DataFrame(solve_dict_ecos).T

df_qoco.to_csv("results/maros/qoco.csv")
df_clarabel.to_csv("results/maros/clarabel.csv")
df_gurobi.to_csv("results/maros/gurobi.csv")
df_mosek.to_csv("results/maros/mosek.csv")
df_ecos.to_csv("results/maros/ecos.csv")
