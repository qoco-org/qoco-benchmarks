from problems.portfolio import portfolio
from problems.group_lasso import group_lasso
from problems.lcvx import lcvx
from problems.oscillating_masses import oscillating_masses
from problems.robust_kalman_filter import robust_kalman_filter

import qoco
import numpy as np
from solvers.cvxpy_to_qoco import convert
from concurrent.futures import ThreadPoolExecutor, as_completed


def call_generate(obj, name):
    obj.generate_solver("./generated_solvers", name)


def generate_lcvx(Nlist):
    np.random.seed(123)
    for N in Nlist:
        name = "lcvx_" + str(N)
        prob = lcvx(N)
        n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
        prob_qoco = qoco.QOCO()
        prob_qoco.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q)
        prob_qoco.generate_solver("./generated_solvers", name)


def generate_oscillating_masses(Nlist):
    np.random.seed(123)
    for N in Nlist:
        name = "oscillating_masses_" + str(N)
        prob, x0, Q, R, A, B, umax, xmax = oscillating_masses(N)
        n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
        prob_qoco = qoco.QOCO()
        prob_qoco.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q)
        prob_qoco.generate_solver("./generated_solvers", name)


def generate_robust_kalman_filter(Nlist):
    np.random.seed(123)
    for N in Nlist:
        name = "robust_kalman_filter_" + str(N)
        prob = robust_kalman_filter(N)
        n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
        prob_qoco = qoco.QOCO()
        prob_qoco.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q)
        prob_qoco.generate_solver("./generated_solvers", name)


def generate_portfolio(Nlist, ninstances):
    np.random.seed(123)
    problems = []
    names = []
    for N in Nlist:
        for i in range(ninstances):
            name = "portfolio_N_" + str(N) + "_i_" + str(i)
            names.append(name)
            prob = portfolio(N)
            n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
            prob_qoco = qoco.QOCO()
            prob_qoco.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q)
            problems.append(prob_qoco)

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(call_generate, obj, name)
            for obj, name in zip(problems, names)
        ]

        for future in as_completed(futures):
            future.result()


def generate_group_lasso(Nlist, ninstances):
    np.random.seed(123)
    problems = []
    names = []
    for N in Nlist:
        for i in range(ninstances):
            name = "group_lasso_N_" + str(N) + "_i_" + str(i)
            names.append(name)
            prob = group_lasso(N)
            n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
            prob_qoco = qoco.QOCO()
            prob_qoco.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q)
            problems.append(prob_qoco)

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(call_generate, obj, name)
            for obj, name in zip(problems, names)
        ]

        for future in as_completed(futures):
            future.result()


# For group lasso and portfolio must generate all custom solvers at the same time in order for them to have the correct
# sparsity structure according to the pseudo random number generator.
ninstances = 20
Ngl = [1, 2, 3, 4, 5]
Nport = [2, 4, 6, 8, 10]
Nlcvx = [15, 50, 75, 100, 125]
Nrkf = [25, 50, 75, 125, 175]
Nom = [8, 20, 32, 44, 56]

generate_portfolio(Nport, ninstances)
generate_group_lasso(Ngl, ninstances)
generate_lcvx(Nlcvx)
generate_oscillating_masses(Nom)
generate_robust_kalman_filter(Nrkf)
