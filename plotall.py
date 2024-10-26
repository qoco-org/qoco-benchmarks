from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
from matplotlib import rc
from utils import get_average_solvetime


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

    qoco_size, qoco_time = get_average_solvetime(df_qoco_robust_kalman_filter)
    qoco_custom_size, qoco_custom_time = get_average_solvetime(df_qoco_custom_robust_kalman_filter)
    clarabel_size, clarabel_time = get_average_solvetime(df_clarabel_robust_kalman_filter)
    gurobi_size, gurobi_time = get_average_solvetime(df_gurobi_robust_kalman_filter)
    mosek_size, mosek_time = get_average_solvetime(df_mosek_robust_kalman_filter)
    ecos_size, ecos_time = get_average_solvetime(df_ecos_robust_kalman_filter)

    plt.figure()
    plt.plot(
        clarabel_size,
        clarabel_time,
        "o-",
        color="darkviolet",
        label="Clarabel",
    )
    plt.plot(
        ecos_size,
        ecos_time,
        "o-",
        color="mediumseagreen",
        label="ECOS",
    )
    plt.plot(
        gurobi_size,
        gurobi_time,
        "o-",
        color="coral",
        label="Gurobi",
    )
    plt.plot(
        mosek_size,
        mosek_time,
        "o-",
        color="firebrick",
        label="Mosek",
    )
    plt.plot(
        qoco_size,
        qoco_time,
        "o-",
        color="royalblue",
        label="QOCO",
    )
    plt.plot(
        qoco_custom_size,
        qoco_custom_time,
        "o-",
        color="palevioletred",
        label="QOCO Custom",
    )
    plt.legend(loc="lower right")
    plt.xlabel("Problem Size")
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

    qoco_size, qoco_time = get_average_solvetime(df_qoco_lcvx)
    qoco_custom_size, qoco_custom_time = get_average_solvetime(df_qoco_custom_lcvx)
    clarabel_size, clarabel_time = get_average_solvetime(df_clarabel_lcvx)
    gurobi_size, gurobi_time = get_average_solvetime(df_gurobi_robust_kalman_filter)
    mosek_size, mosek_time = get_average_solvetime(df_mosek_lcvx)
    ecos_size, ecos_time = get_average_solvetime(df_ecos_lcvx)

    plt.figure()
    plt.plot(
        clarabel_size,
        clarabel_time,
        "o-",
        color="darkviolet",
        label="Clarabel",
    )
    plt.plot(
        ecos_size,
        ecos_time,
        "o-",
        color="mediumseagreen",
        label="ECOS",
    )
    plt.plot(
        gurobi_size,
        gurobi_time,
        "o-",
        color="coral",
        label="Gurobi",
    )
    plt.plot(
        mosek_size,
        mosek_time,
        "o-",
        color="firebrick",
        label="Mosek",
    )
    plt.plot(
        qoco_size,
        qoco_time,
        "o-",
        color="royalblue",
        label="QOCO",
    )
    plt.plot(
        qoco_custom_size,
        qoco_custom_time,
        "o-",
        color="palevioletred",
        label="QOCO Custom",
    )
    plt.legend(loc="lower right")
    plt.xlabel("Problem Size")
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

    qoco_size, qoco_time = get_average_solvetime(df_qoco_portfolio)
    qoco_custom_size, qoco_custom_time = get_average_solvetime(df_qoco_custom_portfolio)
    clarabel_size, clarabel_time = get_average_solvetime(df_clarabel_portfolio)
    gurobi_size, gurobi_time = get_average_solvetime(df_gurobi_portfolio)
    mosek_size, mosek_time = get_average_solvetime(df_mosek_portfolio)
    ecos_size, ecos_time = get_average_solvetime(df_ecos_portfolio)

    plt.figure()
    plt.plot(
        clarabel_size,
        clarabel_time,
        "o-",
        color="darkviolet",
        label="Clarabel",
    )
    plt.plot(
        ecos_size,
        ecos_time,
        "o-",
        color="mediumseagreen",
        label="ECOS",
    )
    plt.plot(
        gurobi_size,
        gurobi_time,
        "o-",
        color="coral",
        label="Gurobi",
    )
    plt.plot(
        mosek_size,
        mosek_time,
        "o-",
        color="firebrick",
        label="Mosek",
    )
    plt.plot(
        qoco_size,
        qoco_time,
        "o-",
        color="royalblue",
        label="QOCO",
    )
    plt.plot(
        qoco_custom_size,
        qoco_custom_time,
        "o-",
        color="palevioletred",
        label="QOCO Custom",
    )
    plt.legend(loc="lower right")
    plt.xlabel("Problem Size")
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

    qoco_size, qoco_time = get_average_solvetime(df_qoco_oscillating_masses)
    qoco_custom_size, qoco_custom_time = get_average_solvetime(df_qoco_custom_oscillating_masses)
    clarabel_size, clarabel_time = get_average_solvetime(df_clarabel_oscillating_masses)
    gurobi_size, gurobi_time = get_average_solvetime(df_gurobi_oscillating_masses)
    mosek_size, mosek_time = get_average_solvetime(df_mosek_oscillating_masses)
    ecos_size, ecos_time = get_average_solvetime(df_ecos_oscillating_masses)
    cvxgen_size, cvxgen_time = get_average_solvetime(df_cvxgen_oscillating_masses)

    plt.figure()
    plt.plot(
        clarabel_size,
        clarabel_time,
        "o-",
        color="darkviolet",
        label="Clarabel",
    )
    plt.plot(
        cvxgen_size,
        cvxgen_time,
        "o-",
        color="olive",
        label="CVXGEN",
    )
    plt.plot(
        ecos_size,
        ecos_time,
        "o-",
        color="mediumseagreen",
        label="ECOS",
    )
    plt.plot(
        gurobi_size,
        gurobi_time,
        "o-",
        color="coral",
        label="Gurobi",
    )
    plt.plot(
        mosek_size,
        mosek_time,
        "o-",
        color="firebrick",
        label="Mosek",
    )
    plt.plot(
        qoco_size,
        qoco_time,
        "o-",
        color="royalblue",
        label="QOCO",
    )
    plt.plot(
        qoco_custom_size,
        qoco_custom_time,
        "o-",
        color="palevioletred",
        label="QOCO Custom",
    )
    plt.legend(loc="lower right")
    plt.xlabel("Problem Size")
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

    qoco_size, qoco_time = get_average_solvetime(df_qoco_group_lasso)
    qoco_custom_size, qoco_custom_time = get_average_solvetime(df_qoco_custom_group_lasso)
    clarabel_size, clarabel_time = get_average_solvetime(df_clarabel_group_lasso)
    gurobi_size, gurobi_time = get_average_solvetime(df_gurobi_group_lasso)
    mosek_size, mosek_time = get_average_solvetime(df_mosek_group_lasso)
    ecos_size, ecos_time = get_average_solvetime(df_ecos_group_lasso)

    plt.figure()
    plt.plot(
        clarabel_size,
        clarabel_time,
        "o-",
        color="darkviolet",
        label="Clarabel",
    )
    plt.plot(
        ecos_size,
        ecos_time,
        "o-",
        color="mediumseagreen",
        label="ECOS",
    )
    plt.plot(
        gurobi_size,
        gurobi_time,
        "o-",
        color="coral",
        label="Gurobi",
    )
    plt.plot(
        mosek_size,
        mosek_time,
        "o-",
        color="firebrick",
        label="Mosek",
    )
    plt.plot(
        qoco_size,
        qoco_time,
        "o-",
        color="royalblue",
        label="QOCO",
    )
    plt.plot(
        qoco_custom_size,
        qoco_custom_time,
        "o-",
        color="palevioletred",
        label="QOCO Custom",
    )
    plt.legend(loc="lower right")
    plt.xlabel("Problem Size")
    plt.ylabel("Solvetime [milliseconds]")
    plt.yscale("log")
    plt.title("Group Lasso")
    strFile = "plots/group_lasso.pdf"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)

    # Sanity check to make sure custom solvers are generated based on the most updated data.
    assert (
        np.linalg.norm(
            df_gurobi_robust_kalman_filter["obj"].values[0:100]
            - df_qoco_custom_robust_kalman_filter["obj"].values[0:100],
            np.inf,
        )
        < 1e-5
    )
    assert (
        np.linalg.norm(
            df_gurobi_lcvx["obj"].values[0:100]
            - df_qoco_custom_lcvx["obj"].values[0:100],
            np.inf,
        )
        < 1e-5
    )
    assert (
        np.linalg.norm(
            df_gurobi_portfolio["obj"].values[0:100]
            - df_qoco_custom_portfolio["obj"].values[0:100],
            np.inf,
        )
        < 1e-5
    )
    assert (
        np.linalg.norm(
            df_gurobi_oscillating_masses["obj"].values[0:100]
            - df_qoco_custom_oscillating_masses["obj"].values[0:100],
            np.inf,
        )
        < 1e-5
    )
    assert (
        np.linalg.norm(
            df_gurobi_oscillating_masses["obj"].values[0:40]
            - df_cvxgen_oscillating_masses["obj"].values[0:40],
            np.inf,
        )
        < 1e-5
    )
    assert (
        np.linalg.norm(
            df_gurobi_group_lasso["obj"].values[0:100]
            - df_qoco_custom_group_lasso["obj"].values[0:100],
            np.inf,
        )
        < 1e-5
    )

    plt.show()
