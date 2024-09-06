import pickle
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from postprocess import *

solvers = ["qcos", "osqp", "clarabel", "piqp"]

with open("mm_qcos_40k.pkl", "rb") as f:
    qcos = pickle.load(f)

with open("mm_osqp_40k.pkl", "rb") as f:
    osqp = pickle.load(f)
with open("mm_clarabel_40k.pkl", "rb") as f:
    clarabel = pickle.load(f)

with open("mm_piqp_40k.pkl", "rb") as f:
    piqp = pickle.load(f)

df_qcos = pd.DataFrame(qcos)
df_osqp = pd.DataFrame(osqp)
df_clarabel = pd.DataFrame(clarabel)
df_piqp = pd.DataFrame(piqp)

num_prob = 0
qcos_solved = 0
osqp_solved = 0
clarabel_solved = 0
piqp_solved = 0

qcos_time = []
osqp_time = []
clarabel_time = []
piqp_time = []

for prob in qcos:
    num_prob += 1
    if qcos[prob]["status"] == "QCOS_SOLVED":
        qcos_solved += 1
        qcos_time.append(qcos[prob]["solve_time"])
    else:
        qcos_time.append(1e2)

for prob in osqp:
    if osqp[prob]["status"] == "solved":
        osqp_solved += 1
        osqp_time.append(osqp[prob]["solve_time"])
    else:
        osqp_time.append(1e2)

for prob in clarabel:
    if clarabel[prob]["status"] == "Solved":
        clarabel_solved += 1
        clarabel_time.append(clarabel[prob]["solve_time"])
    else:
        clarabel_time.append(1e2)

for prob in piqp:
    if piqp[prob]["status"] == "Status.PIQP_SOLVED":
        piqp_solved += 1
        piqp_time.append(piqp[prob]["solve_time"])
    else:
        piqp_time.append(1e2)

print("QCOS Solved " + str(qcos_solved) + " out of " + str(num_prob))
print("OSQP Solved " + str(osqp_solved) + " out of " + str(num_prob))
print("Clarabel Solved " + str(clarabel_solved) + " out of " + str(num_prob))
print("PIQP Solved " + str(piqp_solved) + " out of " + str(num_prob))


n = np.linspace(1, num_prob, num_prob)

plt.figure(dpi=200)
plt.scatter(n, qcos_time, color="blue", label="QCOS")
plt.scatter(n, osqp_time, color="red", label="OSQP")
plt.scatter(n, clarabel_time, color="purple", label="Clarabel")
plt.scatter(n, piqp_time, color="green", label="PIQP")
plt.legend()
plt.yscale("log")
plt.show()
