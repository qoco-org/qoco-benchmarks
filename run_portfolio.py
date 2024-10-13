from problems.portfolio import portfolio
from solvers.solvers import *
import pandas as pd
from matplotlib import pyplot as plt


def run_portfolio(regen_solver):
    Nlist = [2, 5, 8, 12, 15, 20, 25, 30, 35]
    # Nlist = [2, 8, 12]
    var_list = []
    solvers = ["clarabel", "ecos", "qoco_custom", "qoco", "mosek", "gurobi"]
    clarabel_res = {}
    ecos_res = {}
    qoco_res = {}
    qoco_custom_res = {}
    mosek_res = {}
    gurobi_res = {}

    for N in Nlist:
        if N >= 15:
            nruns = 10
        else:
            nruns = 100
        name = "portfolio_" + str(N)
        prob = portfolio(N)
        var_list.append(prob.size_metrics.num_scalar_variables)
        clarabel_res[name] = clarabel_solve(prob, 1e-7, nruns)
        mosek_res[name] = mosek_solve(prob, 1e-7, nruns)
        gurobi_res[name] = gurobi_solve(prob, 1e-7, nruns)
        qoco_res[name] = qoco_solve(prob, 1e-7, nruns)
        ecos_res[name] = ecos_solve(prob, 1e-7, nruns)
        if N <= 15:
            qoco_custom_res[name] = qoco_custom_solve(
                prob, "./generated_solvers", name, regen_solver
            )

    df_qoco = pd.DataFrame(qoco_res).T
    df_qoco_custom = pd.DataFrame(qoco_custom_res).T
    df_clarabel = pd.DataFrame(clarabel_res).T
    df_mosek = pd.DataFrame(mosek_res).T
    df_gurobi = pd.DataFrame(gurobi_res).T
    df_ecos = pd.DataFrame(ecos_res).T

    df_qoco.to_csv("results/portfolio/qoco.csv")
    df_qoco_custom.to_csv("results/portfolio/qoco_custom.csv")
    df_clarabel.to_csv("results/portfolio/clarabel.csv")
    df_mosek.to_csv("results/portfolio/mosek.csv")
    df_gurobi.to_csv("results/portfolio/gurobi.csv")
    df_ecos.to_csv("results/portfolio/ecos.csv")


# compute_performance_profiles(solvers, "./results/robust_kalman_filter")
# df_perf = pd.read_csv("./results/robust_kalman_filter/performance_profiles.csv")
# for s in solvers:
#     plt.plot(df_perf["tau"].values, df_perf[s].values, label=s)
# plt.legend(loc="best")
# plt.ylabel(r"$\rho_{s}$")
# plt.xlabel(r"$\tau$")
# plt.grid()
# plt.xscale("log")
