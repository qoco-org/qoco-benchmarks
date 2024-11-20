import scipy.io
from pathlib import Path
import qoco
import osqp
import clarabel
import scs
import piqp
from parse_mm import *
import pandas as pd
from mm_opt import *
import cvxpy as cp


high_acc = 1e-7
low_acc = 1e-5

solve_dict_qoco = {}
solve_dict_osqp = {}
solve_dict_clarabel = {}
solve_dict_piqp = {}
solve_dict_scs = {}
solve_dict_ecos = {}
directory = Path("mm_problems/MAT_Files")
for file_path in directory.iterdir():
    if file_path.is_file():
        mat = scipy.io.loadmat(file_path)
        problem_name = file_path.stem
        print(file_path)
        if len(mat["lb"]) > 40000:
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
        # if (res_qoco.status == 'QOCO_SOLVED'):
        #     print(abs(res_qoco.obj - OPT_COST_MAP[problem_name]) / abs(OPT_COST_MAP[problem_name]))

        ## ECOS
        # x = cp.Variable(n)
        # obj = cp.Minimize(0.5*cp.quad_form(x, P, True) + q.T @ x)
        # con = [lb <= x, x <= ub, rl <= Amm@x, Amm@x <= ru]
        # prob = cp.Problem(obj, con)
        # try:
        #     obj = prob.solve(solver=cp.ECOS, verbose=True)
        #     solve_dict_ecos[problem_name] = {
        #         "status": "Solved",
        #         "setup_time": np.nan,
        #         "solve_time": prob.solver_stats.solve_time,
        #         "run_time": prob.solver_stats.solve_time,
        #         "obj": obj,
        #     }
        # except:
        #     solve_dict_ecos[problem_name] = {
        #         "status": "FAILED",
        #         "setup_time": np.nan,
        #         "solve_time": np.nan,
        #         "run_time": np.nan,
        #         "obj": obj,
        #     }

        # Clarabel
        # P, c, A, b, p, m, cones = parse_mm_clarabel(mat)
        # settings = clarabel.DefaultSettings()
        # settings.tol_gap_abs = high_acc
        # settings.tol_gap_rel = high_acc
        # settings.tol_feas = high_acc
        # settings.verbose = False
        # solver = clarabel.DefaultSolver(P, c, A, b, cones, settings)
        # res_clarabel = solver.solve()
        # solve_dict_clarabel[problem_name] = {
        #     "status": str(res_clarabel.status),
        #     "setup_time": np.nan,
        #     "solve_time": res_clarabel.solve_time,
        #     "run_time": res_clarabel.solve_time,
        #     "obj": res_clarabel.obj_val,
        # }

df_qoco = pd.DataFrame(solve_dict_qoco).T
df_osqp = pd.DataFrame(solve_dict_osqp).T
df_clarabel = pd.DataFrame(solve_dict_clarabel).T
df_piqp = pd.DataFrame(solve_dict_piqp).T
df_scs = pd.DataFrame(solve_dict_scs).T
# df_ecos = pd.DataFrame(solve_dict_ecos).T

df_qoco.to_csv("results/mm_qoco.csv")
# df_osqp.to_csv("results/mm_osqp.csv")
# df_clarabel.to_csv("results/mm_clarabel.csv")
# df_piqp.to_csv("results/mm_piqp.csv")
# df_scs.to_csv("results/mm_scs.csv")
# df_ecos.to_csv("results/mm_ecos.csv")
