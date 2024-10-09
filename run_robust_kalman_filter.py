from problems.robust_kalman_filter import robust_kalman_filter
from solvers.solvers import *
import pandas as pd
from matplotlib import pyplot as plt

Nlist = [25, 50, 75, 100, 125, 150, 175]
var_list = []

regen_solver = False
clarabel_res = {}
ecos_res = {}
qcos_res = {}
qcos_custom_res = {}

for N in Nlist:
    name = "robust_kalman_filter_" + str(N)
    prob = robust_kalman_filter(N)
    var_list.append(prob.size_metrics.num_scalar_variables)
    clarabel_res[name] = clarabel_solve(prob, 1e-7)
    qcos_res[name] = qcos_solve(prob, 1e-7)
    ecos_res[name] = ecos_solve(prob, 1e-7)
    qcos_custom_res[name] = qcos_custom_solve(
        prob, "./generated_solvers", name, regen_solver
    )

df_qcos = pd.DataFrame(qcos_res).T
df_qcos_custom = pd.DataFrame(qcos_custom_res).T
df_clarabel = pd.DataFrame(clarabel_res).T
df_ecos = pd.DataFrame(ecos_res).T

df_qcos.to_csv("results/robust_kalman_filter/qcos.csv")
df_qcos_custom.to_csv("results/robust_kalman_filter/qcos_custom.csv")
df_clarabel.to_csv("results/robust_kalman_filter/clarabel.csv")
df_ecos.to_csv("results/robust_kalman_filter/ecos.csv")

plt.figure()
plt.plot(var_list, 1000 * df_qcos["run_time"], "o-", label="QCOS")
plt.plot(var_list, 1000 * df_qcos_custom["run_time"], "o-", label="QCOS Custom")
plt.plot(var_list, 1000 * df_ecos["run_time"], "o-", label="ECOS")
plt.plot(var_list, 1000 * df_clarabel["run_time"], "o-", label="Clarabel")
plt.legend()
plt.xlabel("Number of Variables")
plt.ylabel("Solvetime [milliseconds]")
plt.savefig("plots/robust_kalman_filter.pdf")
plt.show()
