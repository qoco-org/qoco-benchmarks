from problems.group_lasso import group_lasso
from solvers.solvers import *
import pandas as pd
from matplotlib import pyplot as plt


def run_group_lasso(regen_solver):
    Nlist = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16]
    var_list = []
    solvers = ["clarabel", "ecos", "qoco_custom", "qoco", "mosek", "gurobi"]
    clarabel_res = {}
    ecos_res = {}
    qoco_res = {}
    qoco_custom_res = {}
    mosek_res = {}
    gurobi_res = {}

    for N in Nlist:
        name = "group_lasso_" + str(N)
        prob = group_lasso(N)
        var_list.append(prob.size_metrics.num_scalar_variables)
        clarabel_res[name] = clarabel_solve(prob, 1e-7)
        mosek_res[name] = mosek_solve(prob, 1e-7)
        gurobi_res[name] = gurobi_solve(prob, 1e-7)
        qoco_res[name] = qoco_solve(prob, 1e-7)
        ecos_res[name] = ecos_solve(prob, 1e-7)
        if N <= 5:
            qoco_custom_res[name] = qoco_custom_solve(
                prob, "./generated_solvers", name, regen_solver
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


# compute_performance_profiles(solvers, "./results/robust_kalman_filter")
# df_perf = pd.read_csv("./results/robust_kalman_filter/performance_profiles.csv")
# for s in solvers:
#     plt.plot(df_perf["tau"].values, df_perf[s].values, label=s)
# plt.legend(loc="best")
# plt.ylabel(r"$\rho_{s}$")
# plt.xlabel(r"$\tau$")
# plt.grid()
# plt.xscale("log")
