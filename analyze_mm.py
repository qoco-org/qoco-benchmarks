from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from postprocess import *

solvers = ["qcos", "osqp", "clarabel", "piqp"]

df_qcos = pd.read_csv("./results/mm_qcos.csv")
df_osqp = pd.read_csv("./results/mm_osqp.csv")
df_clarabel = pd.read_csv("./results/mm_clarabel.csv")
df_piqp = pd.read_csv("./results/mm_piqp.csv")

num_prob = 0
qcos_solved = 0
osqp_solved = 0
clarabel_solved = 0
piqp_solved = 0

qcos_time = []
osqp_time = []
clarabel_time = []
piqp_time = []


for status in df_qcos["status"]:
    num_prob += 1
    if status == "QCOS_SOLVED":
        qcos_solved += 1

for status in df_osqp["status"]:
    if status == "solved":
        osqp_solved += 1

for status in df_clarabel["status"]:
    if status == "Solved":
        clarabel_solved += 1

for status in df_piqp["status"]:
    if status == "Status.PIQP_SOLVED":
        piqp_solved += 1

print("QCOS Solved " + str(qcos_solved) + " out of " + str(num_prob))
print("OSQP Solved " + str(osqp_solved) + " out of " + str(num_prob))
print("Clarabel Solved " + str(clarabel_solved) + " out of " + str(num_prob))
print("PIQP Solved " + str(piqp_solved) + " out of " + str(num_prob))

# Plot performance profile
compute_performance_profiles(solvers)
df_perf = pd.read_csv("./results/mm_performance_profiles.csv")
for s in solvers:
    plt.plot(df_perf["tau"].values, df_perf[s].values, label=s)
plt.legend(loc="best")
plt.ylabel(r"$\rho_{s}$")
plt.xlabel(r"$\tau$")
plt.grid()
plt.xscale("log")
plt.show()
