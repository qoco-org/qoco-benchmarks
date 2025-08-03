import scipy.io
from pathlib import Path
import pandas as pd
from mm_problems.mm_opt import *
from solvers.solvers import *
from mpc.construct_mpc_problem import construct_mpc_problem


solve_dict_qoco = {}
solve_dict_clarabel = {}
solve_dict_gurobi = {}
solve_dict_mosek = {}
solve_dict_ecos = {}
directory = Path("mpc/data")
for file_path in directory.iterdir():
    if file_path.is_file():
        mat = scipy.io.loadmat(file_path, struct_as_record=False, squeeze_me=True)
        problem_name = file_path.stem
        print(problem_name)
        # Set up CVXPY problem.
        prob = construct_mpc_problem(mat)

        # QOCO
        solve_dict_qoco[problem_name] = qoco_solve(prob, 1e-7, N=1)

        # Gurobi
        solve_dict_gurobi[problem_name] = gurobi_solve(prob, 1e-7, N=1)

        # Clarabel
        solve_dict_clarabel[problem_name] = clarabel_solve(prob, 1e-7, N=1)

        # Mosek
        solve_dict_mosek[problem_name] = mosek_solve(prob, 1e-7, N=1)

        # ECOS
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
