from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from postprocess import *
from plotall import *
from utils import *

solvers = ["qoco", "qoco_custom", "clarabel", "ecos", "gurobi", "mosek"]

df_qoco = pd.read_csv("./results/mpc/qoco.csv")
df_qoco_custom = pd.read_csv("./results/mpc/qoco_custom.csv")
df_clarabel = pd.read_csv("./results/mpc/clarabel.csv")
df_ecos = pd.read_csv("./results/mpc/ecos.csv")
df_gurobi = pd.read_csv("./results/mpc/gurobi.csv")
df_mosek = pd.read_csv("./results/mpc/mosek.csv")

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
tmax = 0.51
compute_relative_profile(solvers, tmax, "./results/mpc", xrange=(0, 2.3))
compute_absolute_profile(solvers, tmax, "./results/mpc", xrange=(-5, -1))
compute_shifted_geometric_mean_custom(solvers, tmax, "./results/mpc", "mpc")
make_table(
    solvers,
    "./results/mpc",
    "mpc",
    "Iterations and solver runtimes for mpc problems",
)
plot_performance_curves("mpc",custom=True)

idx = np.where(~np.isnan(df_qoco_custom["obj"].values) == True)
relerror = np.abs(df_gurobi["obj"].values[idx]- df_qoco_custom["obj"].values[idx]) / np.abs(df_gurobi["obj"].values[idx])
assert (
    np.linalg.norm(relerror,np.inf)
    < 1e-3
)
