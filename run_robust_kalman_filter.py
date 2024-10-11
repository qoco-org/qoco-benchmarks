from problems.robust_kalman_filter import robust_kalman_filter
from solvers.solvers import *
import pandas as pd
from matplotlib import pyplot as plt
from postprocess import compute_performance_profiles

Nlist = [25, 50, 75, 100, 125, 150, 175, 300, 500]
var_list = []
solvers = ["clarabel", "ecos", "qcos_custom", "qcos", "mosek"]
regen_solver = False
clarabel_res = {}
ecos_res = {}
qcos_res = {}
qcos_custom_res = {}
mosek_res = {}

for N in Nlist:
    name = "robust_kalman_filter_" + str(N)
    prob = robust_kalman_filter(N)
    var_list.append(prob.size_metrics.num_scalar_variables)
    clarabel_res[name] = clarabel_solve(prob, 1e-7)
    mosek_res[name] = mosek_solve(prob, 1e-7)
    qcos_res[name] = qcos_solve(prob, 1e-7)
    ecos_res[name] = ecos_solve(prob, 1e-7)
    if N <= 175:
        qcos_custom_res[name] = qcos_custom_solve(
            prob, "./generated_solvers", name, regen_solver
        )

df_qcos = pd.DataFrame(qcos_res).T
df_qcos_custom = pd.DataFrame(qcos_custom_res).T
df_clarabel = pd.DataFrame(clarabel_res).T
df_mosek = pd.DataFrame(mosek_res).T
df_ecos = pd.DataFrame(ecos_res).T

df_qcos.to_csv("results/robust_kalman_filter/qcos.csv")
df_qcos_custom.to_csv("results/robust_kalman_filter/qcos_custom.csv")
df_clarabel.to_csv("results/robust_kalman_filter/clarabel.csv")
df_mosek.to_csv("results/robust_kalman_filter/mosek.csv")
df_ecos.to_csv("results/robust_kalman_filter/ecos.csv")

# compute_performance_profiles(solvers, "./results/robust_kalman_filter")
# df_perf = pd.read_csv("./results/robust_kalman_filter/performance_profiles.csv")
# for s in solvers:
#     plt.plot(df_perf["tau"].values, df_perf[s].values, label=s)
# plt.legend(loc="best")
# plt.ylabel(r"$\rho_{s}$")
# plt.xlabel(r"$\tau$")
# plt.grid()
# plt.xscale("log")

plt.figure()
plt.plot(var_list, 1000 * df_qcos["run_time"], "o-", label="QCOS")
plt.plot(var_list[0:7], 1000 * df_qcos_custom["run_time"], "o-", label="QCOS Custom")
plt.plot(var_list, 1000 * df_ecos["run_time"], "o-", label="ECOS")
plt.plot(var_list, 1000 * df_mosek["run_time"], "o-", label="MOSEK")
plt.plot(var_list, 1000 * df_clarabel["run_time"], "o-", label="Clarabel")
plt.legend()
plt.xlabel("Number of Variables")
plt.ylabel("Solvetime [milliseconds]")
plt.savefig("plots/robust_kalman_filter.pdf")
plt.show()
