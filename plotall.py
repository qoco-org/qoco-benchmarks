from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
from matplotlib import rc


def plotall():
    plt.rcParams.update({"text.usetex": True, "font.family": "Helvetica"})

    df_qoco_robust_kalman_filter = pd.read_csv(
        "./results/robust_kalman_filter/qoco.csv"
    )
    df_qoco_custom_robust_kalman_filter = pd.read_csv(
        "./results/robust_kalman_filter/qoco_custom.csv"
    )
    df_clarabel_robust_kalman_filter = pd.read_csv(
        "./results/robust_kalman_filter/clarabel.csv"
    )
    df_mosek_robust_kalman_filter = pd.read_csv(
        "./results/robust_kalman_filter/mosek.csv"
    )
    df_gurobi_robust_kalman_filter = pd.read_csv(
        "./results/robust_kalman_filter/gurobi.csv"
    )
    df_ecos_robust_kalman_filter = pd.read_csv(
        "./results/robust_kalman_filter/ecos.csv"
    )

    plt.figure()
    plt.plot(
        df_ecos_robust_kalman_filter["nvar"],
        1000 * df_ecos_robust_kalman_filter["run_time"],
        "o-",
        color="green",
        label="ECOS",
    )
    plt.plot(
        df_mosek_robust_kalman_filter["nvar"],
        1000 * df_mosek_robust_kalman_filter["run_time"],
        "o-",
        color="red",
        label="MOSEK",
    )
    plt.plot(
        df_gurobi_robust_kalman_filter["nvar"],
        1000 * df_gurobi_robust_kalman_filter["run_time"],
        "o-",
        color="orange",
        label="Gurobi",
    )
    plt.plot(
        df_clarabel_robust_kalman_filter["nvar"],
        1000 * df_clarabel_robust_kalman_filter["run_time"],
        "o-",
        color="purple",
        label="Clarabel",
    )
    plt.plot(
        df_qoco_robust_kalman_filter["nvar"],
        1000 * df_qoco_robust_kalman_filter["run_time"],
        "o-",
        color="blue",
        label="QOCO",
    )
    plt.plot(
        df_qoco_custom_robust_kalman_filter["nvar"],
        1000 * df_qoco_custom_robust_kalman_filter["run_time"],
        "o-",
        color="black",
        label="QOCO Custom",
    )
    plt.legend(loc="lower right")
    plt.xlabel("Number of Variables")
    plt.ylabel("Solvetime [milliseconds]")
    plt.yscale("log")
    plt.title("Robust Kalman Filter")
    strFile = "plots/robust_kalman_filter.pdf"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)

    df_qoco_lcvx = pd.read_csv("./results/lcvx/qoco.csv")
    df_qoco_custom_lcvx = pd.read_csv("./results/lcvx/qoco_custom.csv")
    df_clarabel_lcvx = pd.read_csv("./results/lcvx/clarabel.csv")
    df_mosek_lcvx = pd.read_csv("./results/lcvx/mosek.csv")
    df_gurobi_lcvx = pd.read_csv("./results/lcvx/gurobi.csv")
    df_ecos_lcvx = pd.read_csv("./results/lcvx/ecos.csv")

    plt.figure()
    plt.plot(
        df_ecos_lcvx["nvar"],
        1000 * df_ecos_lcvx["run_time"],
        "o-",
        color="green",
        label="ECOS",
    )
    plt.plot(
        df_mosek_lcvx["nvar"],
        1000 * df_mosek_lcvx["run_time"],
        "o-",
        color="red",
        label="MOSEK",
    )
    plt.plot(
        df_gurobi_lcvx["nvar"],
        1000 * df_gurobi_lcvx["run_time"],
        "o-",
        color="orange",
        label="Gurobi",
    )
    plt.plot(
        df_clarabel_lcvx["nvar"],
        1000 * df_clarabel_lcvx["run_time"],
        "o-",
        color="purple",
        label="Clarabel",
    )
    plt.plot(
        df_qoco_lcvx["nvar"],
        1000 * df_qoco_lcvx["run_time"],
        "o-",
        color="blue",
        label="QOCO",
    )
    plt.plot(
        df_qoco_custom_lcvx["nvar"],
        1000 * df_qoco_custom_lcvx["run_time"],
        "o-",
        color="black",
        label="QOCO Custom",
    )
    top = plt.ylim()[1]
    failed_idx = np.where(df_ecos_lcvx["status"].values != "optimal")
    plt.scatter(
        df_ecos_lcvx["nvar"].values[failed_idx],
        2 * top * np.ones(len(failed_idx[0])),
        color="green",
        marker="x",
    )
    plt.legend(loc="lower right")
    plt.xlabel("Number of Variables")
    plt.ylabel("Solvetime [milliseconds]")
    plt.yscale("log")
    plt.title("LCvx")
    strFile = "plots/lcvx.pdf"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)

    df_qoco_portfolio = pd.read_csv("./results/portfolio/qoco.csv")
    df_qoco_custom_portfolio = pd.read_csv("./results/portfolio/qoco_custom.csv")
    df_clarabel_portfolio = pd.read_csv("./results/portfolio/clarabel.csv")
    df_mosek_portfolio = pd.read_csv("./results/portfolio/mosek.csv")
    df_gurobi_portfolio = pd.read_csv("./results/portfolio/gurobi.csv")
    df_ecos_portfolio = pd.read_csv("./results/portfolio/ecos.csv")

    plt.figure()
    plt.plot(
        df_ecos_portfolio["nvar"],
        1000 * df_ecos_portfolio["run_time"],
        "o-",
        color="green",
        label="ECOS",
    )
    plt.plot(
        df_mosek_portfolio["nvar"],
        1000 * df_mosek_portfolio["run_time"],
        "o-",
        color="red",
        label="MOSEK",
    )
    plt.plot(
        df_gurobi_portfolio["nvar"],
        1000 * df_gurobi_portfolio["run_time"],
        "o-",
        color="orange",
        label="Gurobi",
    )
    plt.plot(
        df_clarabel_portfolio["nvar"],
        1000 * df_clarabel_portfolio["run_time"],
        "o-",
        color="purple",
        label="Clarabel",
    )
    plt.plot(
        df_qoco_portfolio["nvar"],
        1000 * df_qoco_portfolio["run_time"],
        "o-",
        color="blue",
        label="QOCO",
    )
    plt.plot(
        df_qoco_custom_portfolio["nvar"],
        1000 * df_qoco_custom_portfolio["run_time"],
        "o-",
        color="black",
        label="QOCO Custom",
    )
    plt.legend(loc="lower right")
    plt.xlabel("Number of Variables")
    plt.ylabel("Solvetime [milliseconds]")
    plt.yscale("log")
    plt.title("Portfolio Optimization")
    strFile = "plots/portfolio.pdf"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)

    df_qoco_oscillating_masses = pd.read_csv("./results/oscillating_masses/qoco.csv")
    df_qoco_custom_oscillating_masses = pd.read_csv(
        "./results/oscillating_masses/qoco_custom.csv"
    )
    df_clarabel_oscillating_masses = pd.read_csv(
        "./results/oscillating_masses/clarabel.csv"
    )
    df_mosek_oscillating_masses = pd.read_csv("./results/oscillating_masses/mosek.csv")
    df_gurobi_oscillating_masses = pd.read_csv(
        "./results/oscillating_masses/gurobi.csv"
    )
    df_ecos_oscillating_masses = pd.read_csv("./results/oscillating_masses/ecos.csv")
    df_cvxgen_oscillating_masses = pd.read_csv(
        "./results/oscillating_masses/cvxgen.csv"
    )

    plt.figure()
    plt.plot(
        df_ecos_oscillating_masses["nvar"],
        1000 * df_ecos_oscillating_masses["run_time"],
        "o-",
        color="green",
        label="ECOS",
    )
    plt.plot(
        df_mosek_oscillating_masses["nvar"],
        1000 * df_mosek_oscillating_masses["run_time"],
        "o-",
        color="red",
        label="MOSEK",
    )
    plt.plot(
        df_gurobi_oscillating_masses["nvar"],
        1000 * df_gurobi_oscillating_masses["run_time"],
        "o-",
        color="orange",
        label="Gurobi",
    )
    plt.plot(
        df_clarabel_oscillating_masses["nvar"],
        1000 * df_clarabel_oscillating_masses["run_time"],
        "o-",
        color="purple",
        label="Clarabel",
    )
    plt.plot(
        df_qoco_oscillating_masses["nvar"],
        1000 * df_qoco_oscillating_masses["run_time"],
        "o-",
        color="blue",
        label="QOCO",
    )
    plt.plot(
        df_qoco_custom_oscillating_masses["nvar"],
        1000 * df_qoco_custom_oscillating_masses["run_time"],
        "o-",
        color="black",
        label="QOCO Custom",
    )
    plt.plot(
        df_cvxgen_oscillating_masses["nvar"],
        1000 * df_cvxgen_oscillating_masses["run_time"],
        "o-",
        color="steelblue",
        label="CVXGEN",
    )
    top = plt.ylim()[1]
    plt.scatter(
        df_qoco_custom_oscillating_masses["nvar"].values[2:5],
        2 * top * np.ones(3),
        color="steelblue",
        marker="x",
    )
    plt.legend(loc="lower right")
    plt.xlabel("Number of Variables")
    plt.ylabel("Solvetime [milliseconds]")
    plt.yscale("log")
    plt.title("Oscillating Masses")
    strFile = "plots/oscillating_masses.pdf"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)

    df_qoco_group_lasso = pd.read_csv("./results/group_lasso/qoco.csv")
    df_qoco_custom_group_lasso = pd.read_csv("./results/group_lasso/qoco_custom.csv")
    df_clarabel_group_lasso = pd.read_csv("./results/group_lasso/clarabel.csv")
    df_mosek_group_lasso = pd.read_csv("./results/group_lasso/mosek.csv")
    df_gurobi_group_lasso = pd.read_csv("./results/group_lasso/gurobi.csv")
    df_ecos_group_lasso = pd.read_csv("./results/group_lasso/ecos.csv")

    plt.figure()
    plt.plot(
        df_ecos_group_lasso["nvar"],
        1000 * df_ecos_group_lasso["run_time"],
        "o-",
        color="green",
        label="ECOS",
    )
    plt.plot(
        df_mosek_group_lasso["nvar"],
        1000 * df_mosek_group_lasso["run_time"],
        "o-",
        color="red",
        label="MOSEK",
    )
    plt.plot(
        df_gurobi_group_lasso["nvar"],
        1000 * df_gurobi_group_lasso["run_time"],
        "o-",
        color="orange",
        label="Gurobi",
    )
    plt.plot(
        df_clarabel_group_lasso["nvar"],
        1000 * df_clarabel_group_lasso["run_time"],
        "o-",
        color="purple",
        label="Clarabel",
    )
    plt.plot(
        df_qoco_group_lasso["nvar"],
        1000 * df_qoco_group_lasso["run_time"],
        "o-",
        color="blue",
        label="QOCO",
    )
    plt.plot(
        df_qoco_custom_group_lasso["nvar"],
        1000 * df_qoco_custom_group_lasso["run_time"],
        "o-",
        color="black",
        label="QOCO Custom",
    )
    plt.legend(loc="lower right")
    plt.xlabel("Number of Variables")
    plt.ylabel("Solvetime [milliseconds]")
    plt.yscale("log")
    plt.title("Group Lasso")
    strFile = "plots/group_lasso.pdf"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)

    plt.show()
