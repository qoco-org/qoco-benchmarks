from problems.lcvx import lcvx
from solvers.solvers import *
import pandas as pd


def run_lcvx(ninstances, nruns):
    np.random.seed(123)

    Nlist = [15, 50, 75, 100, 125, 150, 200, 250, 300, 350]

    var_list = []
    clarabel_res = {}
    ecos_res = {}
    qoco_res = {}
    qoco_custom_res = {}
    mosek_res = {}
    gurobi_res = {}

    for N in Nlist:
        for i in range(ninstances):
            name = "lcvx_N_" + str(N) + "_i_" + str(i)
            prob = lcvx(N)
            var_list.append(prob.size_metrics.num_scalar_variables)
            clarabel_res[name] = clarabel_solve(prob, 1e-7, nruns)
            mosek_res[name] = mosek_solve(prob, 1e-7, nruns)
            gurobi_res[name] = gurobi_solve(prob, 1e-7, nruns)
            qoco_res[name] = qoco_solve(prob, 1e-7, nruns)
            ecos_res[name] = ecos_solve(prob, 1e-7, nruns)
            if N <= 125:
                qoco_custom_res[name] = qoco_custom_solve(
                    prob, "./generated_solvers", "lcvx_" + str(N), nruns
                )

    df_qoco = pd.DataFrame(qoco_res).T
    df_qoco_custom = pd.DataFrame(qoco_custom_res).T
    df_clarabel = pd.DataFrame(clarabel_res).T
    df_mosek = pd.DataFrame(mosek_res).T
    df_gurobi = pd.DataFrame(gurobi_res).T
    df_ecos = pd.DataFrame(ecos_res).T

    df_qoco.to_csv("results/lcvx/qoco.csv")
    df_qoco_custom.to_csv("results/lcvx/qoco_custom.csv")
    df_clarabel.to_csv("results/lcvx/clarabel.csv")
    df_mosek.to_csv("results/lcvx/mosek.csv")
    df_gurobi.to_csv("results/lcvx/gurobi.csv")
    df_ecos.to_csv("results/lcvx/ecos.csv")
