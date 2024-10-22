from problems.robust_kalman_filter import robust_kalman_filter
from solvers.solvers import *
import pandas as pd


def run_robust_kalman_filter(regen_solver, ninstances, nruns):
    Nlist = [25, 50, 75, 125, 175, 225, 300, 375, 450, 500]
    clarabel_res = {}
    ecos_res = {}
    qoco_res = {}
    qoco_custom_res = {}
    mosek_res = {}
    gurobi_res = {}

    for N in Nlist:
        for i in range(ninstances):
            name = "robust_kalman_filter_N_" + str(N) + "_i_" + str(i)
            prob = robust_kalman_filter(N)
            # clarabel_res[name] = clarabel_solve(prob, 1e-7, nruns)
            # mosek_res[name] = mosek_solve(prob, 1e-7, nruns)
            # gurobi_res[name] = gurobi_solve(prob, 1e-7, nruns)
            # qoco_res[name] = qoco_solve(prob, 1e-7, nruns)
            # ecos_res[name] = ecos_solve(prob, 1e-7, nruns)
            if N <= 175:
                qoco_custom_res[name] = qoco_custom_solve(
                    prob,
                    "./generated_solvers",
                    "robust_kalman_filter_" + str(N),
                    regen_solver,
                    nruns,
                )

    df_qoco = pd.DataFrame(qoco_res).T
    df_qoco_custom = pd.DataFrame(qoco_custom_res).T
    df_clarabel = pd.DataFrame(clarabel_res).T
    df_mosek = pd.DataFrame(mosek_res).T
    df_gurobi = pd.DataFrame(gurobi_res).T
    df_ecos = pd.DataFrame(ecos_res).T

    # df_qoco.to_csv("results/robust_kalman_filter/qoco.csv")
    df_qoco_custom.to_csv("results/robust_kalman_filter/qoco_custom.csv")
    # df_clarabel.to_csv("results/robust_kalman_filter/clarabel.csv")
    # df_mosek.to_csv("results/robust_kalman_filter/mosek.csv")
    # df_gurobi.to_csv("results/robust_kalman_filter/gurobi.csv")
    # df_ecos.to_csv("results/robust_kalman_filter/ecos.csv")


# compute_performance_profiles(solvers, "./results/robust_kalman_filter")
# df_perf = pd.read_csv("./results/robust_kalman_filter/performance_profiles.csv")
# for s in solvers:
#     plt.plot(df_perf["tau"].values, df_perf[s].values, label=s)
# plt.legend(loc="best")
# plt.ylabel(r"$\rho_{s}$")
# plt.xlabel(r"$\tau$")
# plt.grid()
# plt.xscale("log")
