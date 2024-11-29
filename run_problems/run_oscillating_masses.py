from problems.oscillating_masses import oscillating_masses
from solvers.solvers import *
import pandas as pd


def run_oscillating_masses(ninstances, nruns):
    np.random.seed(123)

    Nlist = [8, 20, 32, 44, 56, 76, 96, 116, 136, 156]

    var_list = []
    clarabel_res = {}
    ecos_res = {}
    qoco_res = {}
    qoco_custom_res = {}
    mosek_res = {}
    gurobi_res = {}
    cvxgen_res = {}

    for N in Nlist:
        for i in range(ninstances):
            name = "oscillating_masses_N_" + str(N) + "_i_" + str(i)
            prob, x0, Q, R, A, B, umax, xmax = oscillating_masses(N)
            var_list.append(prob.size_metrics.num_scalar_variables)
            clarabel_res[name] = clarabel_solve(prob, 1e-7, nruns)
            mosek_res[name] = mosek_solve(prob, 1e-7, nruns)
            gurobi_res[name] = gurobi_solve(prob, 1e-7, nruns)
            qoco_res[name] = qoco_solve(prob, 1e-7, nruns)
            ecos_res[name] = ecos_solve(prob, 1e-7, nruns)
            if N <= 56:
                qoco_custom_res[name] = qoco_custom_solve(
                    prob,
                    "./generated_solvers",
                    "oscillating_masses_" + str(N),
                    nruns,
                )
            if N <= 20:
                solved, obj, runtime_sec = run_generated_cvxgen(
                    "./cvxgen/generated_solvers/" + "oscillating_masses_" + str(N),
                    x0,
                    Q,
                    R,
                    A,
                    B,
                    umax,
                    xmax,
                    nruns,
                )
                if solved:
                    cvxgen_res[name] = {
                        "size": get_problem_size(prob),
                        "status": "optimal",
                        "setup_time": None,
                        "solve_time": runtime_sec,
                        "run_time": runtime_sec,
                        "obj": obj,
                    }
                else:
                    cvxgen_res[name] = {
                        "size": get_problem_size(prob),
                        "status": "optimal",
                        "setup_time": None,
                        "solve_time": runtime_sec,
                        "run_time": runtime_sec,
                        "obj": obj,
                    }

    df_qoco = pd.DataFrame(qoco_res).T
    df_qoco_custom = pd.DataFrame(qoco_custom_res).T
    df_clarabel = pd.DataFrame(clarabel_res).T
    df_mosek = pd.DataFrame(mosek_res).T
    df_gurobi = pd.DataFrame(gurobi_res).T
    df_ecos = pd.DataFrame(ecos_res).T
    df_cvxgen = pd.DataFrame(cvxgen_res).T

    df_qoco.to_csv("results/oscillating_masses/qoco.csv")
    df_qoco_custom.to_csv("results/oscillating_masses/qoco_custom.csv")
    df_clarabel.to_csv("results/oscillating_masses/clarabel.csv")
    df_mosek.to_csv("results/oscillating_masses/mosek.csv")
    df_gurobi.to_csv("results/oscillating_masses/gurobi.csv")
    df_ecos.to_csv("results/oscillating_masses/ecos.csv")
    df_cvxgen.to_csv("results/oscillating_masses/cvxgen.csv")
