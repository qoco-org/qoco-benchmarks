import h5py
from pathlib import Path
import pandas as pd
from mm_problems.mm_opt import *
import cvxpy as cp
from solvers.solvers import *
from scipy import sparse

problem_types = ["huber", "lasso"]

# Dont include Springer_ESOC, Rucci_Rucci1, Bates_sls.
# skip = ["ANSYS_Delor64K", "ANSYS_Delor295K", "ANSYS_Delor338K", "NYPA_Maragal_6", "NYPA_Maragal_7", "NYPA_Maragal_8", "Pereyra_landmark", "Springer_ESOC", "Rucci_Rucci1", "Bates_sls"]
skip = [
    "Springer_ESOC",
    "Rucci_Rucci1",
    "Bates_sls",
]

solve_dict_qoco = {}
solve_dict_clarabel = {}
solve_dict_gurobi = {}
solve_dict_mosek = {}
solve_dict_ecos = {}
directory = Path("suitesparse/data")
for file_path in directory.iterdir():
    for problem_type in problem_types:
        if file_path.is_file():
            f = h5py.File(file_path, "r")

            problem_name = file_path.stem + "_" + problem_type
            print(problem_name)

            # Set up CVXPY problem.
            Ax = f["A"]["data"][:]
            Ai = f["A"]["ir"][:]
            Ap = f["A"]["jc"][:]
            b = f["b"][:]

            n = len(Ap) - 1
            m = len(b)
            A = sparse.csc_matrix((Ax, Ai, Ap), shape=(m, n))
            f.close()
            if file_path.stem in skip:
                continue
            x = cp.Variable(n)
            obj = 0
            if problem_type == "huber":
                obj = cp.sum(cp.huber(A @ x - b))
            elif problem_type == "lasso":
                lam = np.linalg.norm(A.T @ b, np.inf)
                obj = cp.sum_squares(A @ x - b) + lam * cp.norm(x, 1)
            else:
                raise ValueError
            prob = cp.Problem(cp.Minimize(obj), [])

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
            df_qoco.to_csv("results/suitesparse/qoco.csv")
            df_clarabel.to_csv("results/suitesparse/clarabel.csv")
            df_gurobi.to_csv("results/suitesparse/gurobi.csv")
            df_mosek.to_csv("results/suitesparse/mosek.csv")
            df_ecos.to_csv("results/suitesparse/ecos.csv")
