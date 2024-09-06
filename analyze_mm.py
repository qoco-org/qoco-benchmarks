import pickle
from matplotlib import pyplot as plt
import numpy as np

with open("mm_qcos_40k.pkl", "rb") as f:
    qcos = pickle.load(f)

with open("mm_osqp_40k.pkl", "rb") as f:
    osqp = pickle.load(f)

with open("mm_clarabel_40k.pkl", "rb") as f:
    clarabel = pickle.load(f)

with open("mm_piqp_40k.pkl", "rb") as f:
    piqp = pickle.load(f)

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
    if qcos[prob].status == "QCOS_SOLVED":
        qcos_solved += 1
        qcos_time.append(qcos[prob].setup_time_sec + qcos[prob].solve_time_sec)
    else:
        qcos_time.append(1e2)

for prob in osqp:
    if osqp[prob].status == "solved":
        osqp_solved += 1
        osqp_time.append(osqp[prob].setup_time_sec + osqp[prob].solve_time_sec)
    else:
        osqp_time.append(1e2)
     
for prob in clarabel:
    if clarabel[prob].status == "Solved":
        clarabel_solved += 1
        clarabel_time.append(clarabel[prob].solve_time_sec)
    else:
        clarabel_time.append(1e2)


for prob in piqp:
    if piqp[prob].status == "Status.PIQP_SOLVED":
        piqp_solved += 1
        piqp_time.append(piqp[prob].solve_time_sec)
    else:
        piqp_time.append(1e2)


print("QCOS Solved " + str(qcos_solved) + " out of " + str(num_prob))
print("OSQP Solved " + str(osqp_solved) + " out of " + str(num_prob))
print("Clarabel Solved " + str(clarabel_solved) + " out of " + str(num_prob))
print("PIQP Solved " + str(piqp_solved) + " out of " + str(num_prob))


n = np.linspace(1, num_prob, num_prob)

plt.figure(dpi=200)
plt.scatter(n, qcos_time, color='blue')
plt.scatter(n, osqp_time, color='red')
plt.scatter(n, clarabel_time, color='purple')
plt.scatter(n, piqp_time, color='green')
plt.yscale('log')
plt.show()
# breakpoint()
