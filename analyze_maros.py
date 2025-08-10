from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from postprocess import *
from plotall import *
from utils import *

solvers = ["qoco", "clarabel", "ecos", "gurobi", "mosek"]

df_qoco = pd.read_csv("./results/maros/qoco.csv")
df_clarabel = pd.read_csv("./results/maros/clarabel.csv")
df_ecos = pd.read_csv("./results/maros/ecos.csv")
df_gurobi = pd.read_csv("./results/maros/gurobi.csv")
df_mosek = pd.read_csv("./results/maros/mosek.csv")

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
compute_relative_profile(solvers, tmax, "./results/maros", xrange=(0, 3.1))
compute_absolute_profile(solvers, tmax, "./results/maros", xrange=(-5, 3))
compute_shifted_geometric_mean(solvers, tmax, "./results/maros", "maros")
make_table(
    solvers,
    "./results/maros",
    "maros",
    "Iterations and solver runtimes for Maros–Mészáros problems",
)
plot_performance_curves("maros")