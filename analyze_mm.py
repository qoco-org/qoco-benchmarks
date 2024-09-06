import pickle

with open('mm_qcos_40k.pkl', 'rb') as f:
    qcos = pickle.load(f)

with open('mm_osqp_40k.pkl', 'rb') as f:
    osqp = pickle.load(f)

num_prob = 0
qcos_solved = 0
osqp_solved = 0

for prob in qcos:
    num_prob += 1
    if qcos[prob].status == 'QCOS_SOLVED':
        qcos_solved += 1

for prob in osqp:
    if osqp[prob].status == 'solved':
        osqp_solved += 1

print("QCOS Solved " + str(qcos_solved) + " out of " + str(num_prob))
print("OSQP Solved " + str(osqp_solved) + " out of " + str(num_prob))