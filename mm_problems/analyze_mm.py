from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
# from postprocess import *

solvers = ["qoco", "clarabel", "gurobi", "mosek"]

df_qoco = pd.read_csv("./results/maros/qoco.csv")
df_clarabel = pd.read_csv("./results/maros/clarabel.csv")
df_gurobi = pd.read_csv("./results/maros/gurobi.csv")
df_mosek = pd.read_csv("./results/maros/mosek.csv")

num_prob = 0
qoco_solved = 0
clarabel_solved = 0
gurobi_solved = 0
mosek_solved = 0

qoco_time = []
clarabel_time = []
gurobi_time = []
mosek_time = []

for status in df_qoco["status"]:
    num_prob += 1
    if status == "QOCO_SOLVED":
        qoco_solved += 1

for status in df_clarabel["status"]:
    if status == "Solved":
        clarabel_solved += 1

for status in df_gurobi["status"]:
    if status == "optimal":
        gurobi_solved += 1

for status in df_mosek["status"]:
    if status == "optimal":
        mosek_solved += 1


print("QOCO Solved " + str(qoco_solved) + " out of " + str(num_prob))
print("Clarabel Solved " + str(clarabel_solved) + " out of " + str(num_prob))
print("Gurobi Solved " + str(gurobi_solved) + " out of " + str(num_prob))
print("Mosek Solved " + str(mosek_solved) + " out of " + str(num_prob))

# Plot performance profile
# compute_performance_profiles(solvers, "./results")
# df_perf = pd.read_csv("./results/performance_profiles.csv")
# for s in solvers:
#     plt.plot(df_perf["tau"].values, df_perf[s].values, label=s)
# plt.legend(loc="best")
# plt.ylabel(r"$\rho_{s}$")
# plt.xlabel(r"$\tau$")
# plt.grid()
# plt.xscale("log")
# plt.savefig("plots/mm.pdf")
# plt.show()
