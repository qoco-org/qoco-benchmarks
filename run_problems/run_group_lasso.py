from problems.group_lasso import group_lasso
from solvers.solvers import *
import pandas as pd


def run_group_lasso(ninstances, nruns):
    np.random.seed(123)

    Nlist = [1, 2, 3, 4, 5, 8, 10, 12, 14, 16]
    var_list = []
    clarabel_res = {}
    ecos_res = {}
    qoco_res = {}
    qoco_custom_res = {}
    mosek_res = {}
    gurobi_res = {}
    for N in Nlist:
        for i in range(ninstances):
            name = "group_lasso_N_" + str(N) + "_i_" + str(i)
            prob = group_lasso(N)
            var_list.append(prob.size_metrics.num_scalar_variables)
            clarabel_res[name] = clarabel_solve(prob, 1e-7, nruns)
            mosek_res[name] = mosek_solve(prob, 1e-7, nruns)
            gurobi_res[name] = gurobi_solve(prob, 1e-7, nruns)
            qoco_res[name] = qoco_solve(prob, 1e-7, nruns)
            ecos_res[name] = ecos_solve(prob, 1e-7, nruns)
            if N <= 5:
                qoco_custom_res[name] = qoco_custom_solve(
                    prob, "./generated_solvers", name, nruns
                )

    df_qoco = pd.DataFrame(qoco_res).T
    df_qoco_custom = pd.DataFrame(qoco_custom_res).T
    df_clarabel = pd.DataFrame(clarabel_res).T
    df_mosek = pd.DataFrame(mosek_res).T
    df_gurobi = pd.DataFrame(gurobi_res).T
    df_ecos = pd.DataFrame(ecos_res).T

    df_qoco.to_csv("results/group_lasso/qoco.csv")
    df_qoco_custom.to_csv("results/group_lasso/qoco_custom.csv")
    df_clarabel.to_csv("results/group_lasso/clarabel.csv")
    df_mosek.to_csv("results/group_lasso/mosek.csv")
    df_gurobi.to_csv("results/group_lasso/gurobi.csv")
    df_ecos.to_csv("results/group_lasso/ecos.csv")
