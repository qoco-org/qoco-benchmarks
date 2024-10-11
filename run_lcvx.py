from problems.optimal_control import lcvx
from solvers.solvers import *
import pandas as pd
from matplotlib import pyplot as plt
from postprocess import compute_performance_profiles

Nlist = [15, 25, 50, 75, 100, 125, 150, 200, 250, 300]
var_list = []
solvers = ["clarabel", "ecos", "qcos_custom", "qcos", "mosek"]
regen_solver = False
clarabel_res = {}
ecos_res = {}
qcos_res = {}
qcos_custom_res = {}
mosek_res = {}

for N in Nlist:
    name = "lcvx_" + str(N)
    prob = lcvx(N)
    var_list.append(prob.size_metrics.num_scalar_variables)
    clarabel_res[name] = clarabel_solve(prob, 1e-7)
    mosek_res[name] = mosek_solve(prob, 1e-7)
    qcos_res[name] = qcos_solve(prob, 1e-7)
    ecos_res[name] = ecos_solve(prob, 1e-7)
    if N <= 125:
        qcos_custom_res[name] = qcos_custom_solve(
            prob, "./generated_solvers", name, regen_solver
        )

df_qcos = pd.DataFrame(qcos_res).T
df_qcos_custom = pd.DataFrame(qcos_custom_res).T
df_clarabel = pd.DataFrame(clarabel_res).T
df_mosek = pd.DataFrame(mosek_res).T
df_ecos = pd.DataFrame(ecos_res).T

df_qcos.to_csv("results/lcvx/qcos.csv")
df_qcos_custom.to_csv("results/lcvx/qcos_custom.csv")
df_clarabel.to_csv("results/lcvx/clarabel.csv")
df_mosek.to_csv("results/lcvx/mosek.csv")
df_ecos.to_csv("results/lcvx/ecos.csv")

# compute_performance_profiles(solvers, "./results/lcvx")
# df_perf = pd.read_csv("./results/lcvx/performance_profiles.csv")
# for s in solvers:
#     plt.plot(df_perf["tau"].values, df_perf[s].values, label=s)
# plt.legend(loc="best")
# plt.ylabel(r"$\rho_{s}$")
# plt.xlabel(r"$\tau$")
# plt.grid()
# plt.xscale("log")
