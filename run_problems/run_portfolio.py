from problems.portfolio import portfolio
from solvers.solvers import *
import pandas as pd
from matplotlib import pyplot as plt


def run_portfolio(regen_solver, ninstances, nruns):
    np.random.seed(123)

    Nlist = [2, 4, 6, 8, 10, 15, 20, 25, 30, 35]
    var_list = []
    clarabel_res = {}
    ecos_res = {}
    qoco_res = {}
    qoco_custom_res = {}
    mosek_res = {}
    gurobi_res = {}

    for N in Nlist:
        for i in range(ninstances):
            name = "portfolio_N_" + str(N) + "_i_" + str(i)
            prob = portfolio(N)
            var_list.append(prob.size_metrics.num_scalar_variables)
            clarabel_res[name] = clarabel_solve(prob, 1e-7, nruns)
            mosek_res[name] = mosek_solve(prob, 1e-7, nruns)
            gurobi_res[name] = gurobi_solve(prob, 1e-7, nruns)
            qoco_res[name] = qoco_solve(prob, 1e-7, nruns)
            ecos_res[name] = ecos_solve(prob, 1e-7, nruns)
            if N <= 10:
                qoco_custom_res[name] = qoco_custom_solve(
                    prob, "./generated_solvers", name, regen_solver, nruns
                )

    df_qoco = pd.DataFrame(qoco_res).T
    df_qoco_custom = pd.DataFrame(qoco_custom_res).T
    df_clarabel = pd.DataFrame(clarabel_res).T
    df_mosek = pd.DataFrame(mosek_res).T
    df_gurobi = pd.DataFrame(gurobi_res).T
    df_ecos = pd.DataFrame(ecos_res).T

    df_qoco.to_csv("results/portfolio/qoco.csv")
    df_qoco_custom.to_csv("results/portfolio/qoco_custom.csv")
    df_clarabel.to_csv("results/portfolio/clarabel.csv")
    df_mosek.to_csv("results/portfolio/mosek.csv")
    df_gurobi.to_csv("results/portfolio/gurobi.csv")
    df_ecos.to_csv("results/portfolio/ecos.csv")
