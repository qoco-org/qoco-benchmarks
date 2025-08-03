import scipy.io
from pathlib import Path
import pandas as pd
from mm_problems.mm_opt import *
from solvers.solvers import *
from mpc.construct_mpc_problem import construct_mpc_problem

NRUNS = 100

solve_dict_qoco = {}
solve_dict_qoco_custom = {}
solve_dict_clarabel = {}
solve_dict_gurobi = {}
solve_dict_mosek = {}
solve_dict_ecos = {}
directory = Path("mpc/data")
for file_path in directory.iterdir():
    if file_path.is_file():
        mat = scipy.io.loadmat(file_path, struct_as_record=False, squeeze_me=True)
        problem_name = file_path.stem
        name = problem_name.removeprefix("matFiles_")
        print(name)
        # Set up CVXPY problem.
        prob = construct_mpc_problem(mat)

        # QOCO
        solve_dict_qoco[name] = qoco_solve(prob, 1e-7, N=NRUNS)

        # QOCO Custom
        solve_dict_qoco_custom[name] = qoco_custom_solve(
            prob,
            "./generated_solvers",
            name,
            NRUNS,
        )

        # Gurobi
        solve_dict_gurobi[name] = gurobi_solve(prob, 1e-7, N=NRUNS)

        # Clarabel
        solve_dict_clarabel[name] = clarabel_solve(prob, 1e-7, N=NRUNS)

        # Mosek
        solve_dict_mosek[name] = mosek_solve(prob, 1e-7, N=NRUNS)

        # ECOS
        solve_dict_ecos[name] = ecos_solve(prob, 1e-7, N=NRUNS)

        # Incrementally save data in case of failure.
        df_qoco = pd.DataFrame(solve_dict_qoco).T
        df_qoco_custom = pd.DataFrame(solve_dict_qoco_custom).T
        df_clarabel = pd.DataFrame(solve_dict_clarabel).T
        df_gurobi = pd.DataFrame(solve_dict_gurobi).T
        df_mosek = pd.DataFrame(solve_dict_mosek).T
        df_ecos = pd.DataFrame(solve_dict_ecos).T
        df_qoco.to_csv("results/mpc/qoco.csv")
        df_qoco_custom.to_csv("results/mpc/qoco_custom.csv")
        df_clarabel.to_csv("results/mpc/clarabel.csv")
        df_gurobi.to_csv("results/mpc/gurobi.csv")
        df_mosek.to_csv("results/mpc/mosek.csv")
        df_ecos.to_csv("results/mpc/ecos.csv")

# Save data at the end since the continue will skip over the final data save in the loop, since the last problem is CONT-300.
df_qoco = pd.DataFrame(solve_dict_qoco).T
df_qoco_custom = pd.DataFrame(solve_dict_qoco_custom).T
df_clarabel = pd.DataFrame(solve_dict_clarabel).T
df_gurobi = pd.DataFrame(solve_dict_gurobi).T
df_mosek = pd.DataFrame(solve_dict_mosek).T
df_ecos = pd.DataFrame(solve_dict_ecos).T
df_qoco.to_csv("results/mpc/qoco.csv")
df_qoco_custom.to_csv("results/mpc/qoco_custom.csv")
df_clarabel.to_csv("results/mpc/clarabel.csv")
df_gurobi.to_csv("results/mpc/gurobi.csv")
df_mosek.to_csv("results/mpc/mosek.csv")
df_ecos.to_csv("results/mpc/ecos.csv")
