from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from postprocess import *
from plotall import *
from utils import *

solvers = ["qoco", "clarabel", "ecos", "gurobi", "mosek"]

df_qoco = pd.read_csv("./results/suitesparse/qoco.csv")
df_clarabel = pd.read_csv("./results/suitesparse/clarabel.csv")
df_ecos = pd.read_csv("./results/suitesparse/ecos.csv")
df_gurobi = pd.read_csv("./results/suitesparse/gurobi.csv")
df_mosek = pd.read_csv("./results/suitesparse/mosek.csv")

num_prob = 0
qoco_solved = 0
clarabel_solved = 0
ecos_solved = 0
gurobi_solved = 0
mosek_solved = 0

for status in df_qoco["status"]:
    num_prob += 1
    if status == "QOCO_SOLVED":
        qoco_solved += 1

for status in df_clarabel["status"]:
    if status == "optimal":
        clarabel_solved += 1

for status in df_ecos["status"]:
    if status == "optimal":
        ecos_solved += 1

for status in df_gurobi["status"]:
    if status == "optimal":
        gurobi_solved += 1

for status in df_mosek["status"]:
    if status == "optimal":
        mosek_solved += 1

print("QOCO Solved " + str(qoco_solved) + " out of " + str(num_prob))
print("Clarabel Solved " + str(clarabel_solved) + " out of " + str(num_prob))
print("ECOS Solved " + str(ecos_solved) + " out of " + str(num_prob))
print("Gurobi Solved " + str(gurobi_solved) + " out of " + str(num_prob))
print("Mosek Solved " + str(mosek_solved) + " out of " + str(num_prob))

idx = np.where(df_qoco["status"].values != "QOCO_SOLVED")
qoco_failed = df_qoco.iloc[idx]["Unnamed: 0"].values
print("QOCO Failed:", qoco_failed)

# Plot performance profile
tmax = 1200.01
compute_relative_profile(solvers, tmax, "./results/suitesparse", xrange=(0, 3.1))
compute_absolute_profile(solvers, tmax, "./results/suitesparse", xrange=(-5, 3))
compute_shifted_geometric_mean(solvers, tmax, "./results/suitesparse", "suitesparse")
make_table(
    solvers,
    "./results/suitesparse",
    "suitesparse",
    "Iterations and solver runtimes for SuiteSparse problems",
)

# Plot performance profiles
df_perf = pd.read_csv("./results/suitesparse/relative_profile.csv")
plt.figure(dpi=200)
plt.plot(
    df_perf["tau"].values,
    df_perf["clarabel"].values,
    color="darkviolet",
    label="Clarabel",
)
plt.plot(
    df_perf["tau"].values, df_perf["ecos"].values, color="mediumseagreen", label="ECOS",
)
plt.plot(
    df_perf["tau"].values, df_perf["gurobi"].values, color="coral", label="Gurobi",
)
plt.plot(
    df_perf["tau"].values, df_perf["mosek"].values, color="firebrick", label="Mosek",
)
plt.plot(
    df_perf["tau"].values, df_perf["qoco"].values, color="royalblue", label="QOCO",
)

plt.legend(loc="lower right")
plt.ylabel("Ratio of problem solved", usetex=True)
plt.xlabel("Performance ratio", usetex=True)
plt.grid()
plt.xscale("log")
plt.title("Performance Ratio", usetex=True)
strFile = "plots/suitesparse_relative_profile.pdf"
if os.path.isfile(strFile):
    os.remove(strFile)
plt.savefig(strFile)

df_perf = pd.read_csv("./results/suitesparse/absolute_profile.csv")
plt.figure(dpi=200)
plt.plot(
    df_perf["tau"].values,
    df_perf["clarabel"].values,
    color="darkviolet",
    label="Clarabel",
)
plt.plot(
    df_perf["tau"].values, df_perf["ecos"].values, color="mediumseagreen", label="ECOS",
)
plt.plot(
    df_perf["tau"].values, df_perf["gurobi"].values, color="coral", label="Gurobi",
)
plt.plot(
    df_perf["tau"].values, df_perf["mosek"].values, color="firebrick", label="Mosek",
)
plt.plot(
    df_perf["tau"].values, df_perf["qoco"].values, color="royalblue", label="QOCO",
)

plt.legend(loc="lower right")
plt.ylabel("Fraction of problem solved within t", usetex=True)
plt.xlabel("Solvetime t [seconds]", usetex=True)
plt.grid()
plt.xscale("log")
plt.title("Solution Time Profile", usetex=True)
strFile = "plots/suitesparse_absolute_profile.pdf"
if os.path.isfile(strFile):
    os.remove(strFile)
plt.savefig(strFile)
