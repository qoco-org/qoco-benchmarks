import scipy.io
from pathlib import Path
import pandas as pd
from mm_problems.mm_opt import *
import cvxpy as cp
from solvers.solvers import *
from utils import parse_maros


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
        print(problem_name)

        # List of problems for ECOS and MOSEK to skip. Both require linear objectives and for problems in this list, 
        # cvxpy returns SIGKILL when parsing problem into one with linear objective, or takes >1200 secs to parse (CONT-201).
        skip_probs = ["BOYD2", "CONT-300", "CONT-201"]

        # cvxpy can parse these for ecos but ecos takes over 1200 secs to solve these problems.
        # Since we cannot impose a time limit on ecos in settings, we skip these problems
        ecos_skip = ["CVXQP1_L", "CVXQP2_L", "CVXQP3_L"] 

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
        solve_dict_gurobi[problem_name] = gurobi_solve(prob, 1e-7, N=1)

        # Clarabel
        solve_dict_clarabel[problem_name] = clarabel_solve(prob, 1e-7, N=1)

        if problem_name in skip_probs:
            fail = {
                "size": get_problem_size(prob),
                "status": np.nan,
                "setup_time": np.nan,
                "solve_time": np.nan,
                "run_time": np.nan,
                "obj": np.nan,
                "iters": np.nan,
            }
            solve_dict_mosek[problem_name] = fail
            solve_dict_ecos[problem_name] = fail
            continue

        # Mosek
        solve_dict_mosek[problem_name] = mosek_solve(prob, 1e-7, N=1)

        # ECOS
        if problem_name in ecos_skip:
            fail = {
                "size": get_problem_size(prob),
                "status": np.nan,
                "setup_time": np.nan,
                "solve_time": np.nan,
                "run_time": np.nan,
                "obj": np.nan,
                "iters": np.nan,
            }
            solve_dict_ecos[problem_name] = fail
            continue
        solve_dict_ecos[problem_name] = ecos_solve(prob, 1e-7, N=1)

        # Incrementally save data in case of failure.
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

# Save data at the end since the continue will skip over the final data save in the loop, since the last problem is CONT-300.
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
