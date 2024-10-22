from problems.portfolio import portfolio
from problems.group_lasso import group_lasso

import qoco
from solvers.cvxpy_to_qoco import convert
from concurrent.futures import ThreadPoolExecutor, as_completed


def call_generate(obj, name):
    obj.generate_solver("./generated_solvers", name)


def generate_portfolio(Nlist, ninstances):
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


ninstances = 20
Ngl = [1, 2, 3, 4, 5]
Nport = [2, 5, 8, 12, 15]
generate_portfolio(Nport, ninstances)
generate_group_lasso(Ngl, ninstances)
