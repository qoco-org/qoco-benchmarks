import scipy.io
from pathlib import Path
import qcospy as qcos
import osqp
import clarabel
import piqp
from parse_mm import *
import pandas as pd
from mm_opt import *
import cvxpy as cp
from cvxpy_to_qcos import *

high_acc = 1e-7
low_acc = 1e-5

solve_dict_qcos = {}
solve_dict_osqp = {}
solve_dict_clarabel = {}
solve_dict_piqp = {}
solve_dict_ecos = {}
directory = Path("mm_problems/MAT_Files")
for file_path in directory.iterdir():
    if file_path.is_file():
        mat = scipy.io.loadmat(file_path)
        problem_name = file_path.stem
        print(file_path)
        if len(mat["lb"]) > 40000:
            continue
        n, m, p, P, c, A, b, G, h, l, nsoc, q = parse_mm_qcos(mat)
        G = G if m > 0 else None
        h = h if m > 0 else None
        A = A if p > 0 else None
        b = b if p > 0 else None
        prob_qcos = qcos.QCOS()
        prob_qcos.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q)
        res_qcos = prob_qcos.solve()
        solve_dict_qcos[problem_name] = {
            "status": res_qcos.status,
            "setup_time": res_qcos.setup_time_sec,
            "solve_time": res_qcos.solve_time_sec,
            "run_time": res_qcos.setup_time_sec + res_qcos.solve_time_sec,
            "obj": res_qcos.obj,
        }
        # if (res_qcos.status == 'QCOS_SOLVED'):
        #     print(abs(res_qcos.obj - OPT_COST_MAP[problem_name]) / abs(OPT_COST_MAP[problem_name]))

        # if (str(status) == 'Status.PIQP_SOLVED'):
        #     print(abs(solver.result.info.primal_obj - OPT_COST_MAP[problem_name]) / abs(OPT_COST_MAP[problem_name]))

        P, q, A, l, u = parse_mm_osqp(mat)
        m = osqp.OSQP()
        m.setup(P=P, q=q, A=A, l=l, u=u, eps_abs=high_acc, eps_rel=high_acc, verbose=False)
        res_osqp = m.solve()
        solve_dict_osqp[problem_name] = {
            "status": res_osqp.info.status,
            "setup_time": res_osqp.info.setup_time,
            "solve_time": res_osqp.info.solve_time,
            "run_time": res_osqp.info.setup_time + res_osqp.info.solve_time,
            "obj": res_osqp.info.obj_val,
        }

        
        ### CVXPY Clarabel
        # n = len(mat["lb"])
        # P = mat["Q"]
        # q = np.squeeze(mat["c"], axis=1)
        # Amm = mat["A"]
        # rl = np.squeeze(mat["rl"], axis=1)
        # ru = np.squeeze(mat["ru"], axis=1)
        # lb = np.squeeze(mat["lb"], axis=1)
        # ub = np.squeeze(mat["ub"], axis=1)
        # x = cp.Variable(n)
        # obj = cp.Minimize(0.5*cp.quad_form(x, P, True) + q.T @ x)
        # con = [lb <= x, x <= ub, rl <= Amm@x, Amm@x <= ru]
        # prob = cp.Problem(obj, con)   
        # try:
        #     obj = prob.solve(solver=cp.CLARABEL)
        #     solve_dict_clarabel[problem_name] = {
        #         "status": "Solved",
        #         "setup_time": np.nan,
        #         "solve_time": prob.solver_stats.solve_time,
        #         "run_time": prob.solver_stats.solve_time,
        #         "obj": obj,
        #     }
        # except:
        #     solve_dict_clarabel[problem_name] = {
        #         "status": "FAILED",
        #         "setup_time": np.nan,
        #         "solve_time": np.nan,
        #         "run_time": np.nan,
        #         "obj": obj,
        #     }


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

        P, q, A, b, cones = parse_mm_clarabel(mat)
        settings = clarabel.DefaultSettings()
        settings.tol_gap_abs = high_acc
        settings.tol_gap_rel = high_acc
        settings.tol_feas = high_acc
        settings.verbose = False
        solver = clarabel.DefaultSolver(P, q, A, b, cones, settings)
        res_clarabel = solver.solve()
        solve_dict_clarabel[problem_name] = {
            "status": str(res_clarabel.status),
            "setup_time": np.nan,
            "solve_time": res_clarabel.solve_time,
            "run_time": res_clarabel.solve_time,
            "obj": res_clarabel.obj_val,
        }

        P, c, A, b, G, h, x_lb, x_ub = parse_mm_piqp(mat)
        solver = piqp.SparseSolver()
        solver.settings.compute_timings = True
        solver.settings.eps_abs = high_acc
        solver.settings.eps_rel = high_acc
        solver.settings.eps_duality_gap_abs = high_acc
        solver.settings.eps_duality_gap_rel = high_acc

        solver.setup(P, c, A, b, G, h, x_lb, x_ub)
        status = solver.solve()
        solve_dict_piqp[problem_name] = {
            "status": str(status),
            "setup_time": np.nan,
            "solve_time": solver.result.info.run_time,
            "run_time": solver.result.info.run_time,
            "obj": solver.result.info.primal_obj,
        }

df_qcos = pd.DataFrame(solve_dict_qcos).T
df_osqp = pd.DataFrame(solve_dict_osqp).T
df_clarabel = pd.DataFrame(solve_dict_clarabel).T
df_piqp = pd.DataFrame(solve_dict_piqp).T
# df_ecos = pd.DataFrame(solve_dict_ecos).T

df_qcos.to_csv("results/mm_qcos.csv")
df_osqp.to_csv("results/mm_osqp.csv")
df_clarabel.to_csv("results/mm_clarabel.csv")
df_piqp.to_csv("results/mm_piqp.csv")
# df_ecos.to_csv("results/mm_ecos.csv")
