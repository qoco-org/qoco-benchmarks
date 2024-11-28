from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
from matplotlib import rc
from utils import get_average_solvetime


def plotall():
    plt.rcParams.update({"text.usetex": True, "font.family": "serif"})

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
    qoco_custom_size, qoco_custom_time = get_average_solvetime(
        df_qoco_custom_robust_kalman_filter
    )
    clarabel_size, clarabel_time = get_average_solvetime(
        df_clarabel_robust_kalman_filter
    )
    gurobi_size, gurobi_time = get_average_solvetime(df_gurobi_robust_kalman_filter)
    mosek_size, mosek_time = get_average_solvetime(df_mosek_robust_kalman_filter)
    ecos_size, ecos_time = get_average_solvetime(df_ecos_robust_kalman_filter)

    plt.figure(figsize=(8.5, 11))
    plt.subplot(321)
    plt.plot(
        clarabel_size, clarabel_time, "o-", color="darkviolet", label="Clarabel",
    )
    plt.plot(
        ecos_size, ecos_time, "o-", color="mediumseagreen", label="ECOS",
    )
    plt.plot(
        gurobi_size, gurobi_time, "o-", color="coral", label="Gurobi",
    )
    plt.plot(
        mosek_size, mosek_time, "o-", color="firebrick", label="Mosek",
    )
    plt.plot(
        qoco_size, qoco_time, "X-", color="royalblue", label="QOCO",
    )
    plt.plot(
        qoco_custom_size,
        qoco_custom_time,
        "X-",
        color="mediumvioletred",
        label="QOCO Custom",
    )
    plt.yscale("log")
    plt.title("Robust Kalman Filter", usetex=True)

    df_qoco_lcvx = pd.read_csv("./results/lcvx/qoco.csv")
    df_qoco_custom_lcvx = pd.read_csv("./results/lcvx/qoco_custom.csv")
    df_clarabel_lcvx = pd.read_csv("./results/lcvx/clarabel.csv")
    df_mosek_lcvx = pd.read_csv("./results/lcvx/mosek.csv")
    df_gurobi_lcvx = pd.read_csv("./results/lcvx/gurobi.csv")
    df_ecos_lcvx = pd.read_csv("./results/lcvx/ecos.csv")

    qoco_size, qoco_time = get_average_solvetime(df_qoco_lcvx)
    qoco_custom_size, qoco_custom_time = get_average_solvetime(df_qoco_custom_lcvx)
    clarabel_size, clarabel_time = get_average_solvetime(df_clarabel_lcvx)
    gurobi_size, gurobi_time = get_average_solvetime(df_gurobi_lcvx)
    mosek_size, mosek_time = get_average_solvetime(df_mosek_lcvx)
    ecos_size, ecos_time = get_average_solvetime(df_ecos_lcvx)

    plt.subplot(322)
    plt.plot(
        clarabel_size, clarabel_time, "o-", color="darkviolet", label="Clarabel",
    )
    plt.plot(
        ecos_size, ecos_time, "o-", color="mediumseagreen", label="ECOS",
    )
    plt.plot(
        gurobi_size, gurobi_time, "o-", color="coral", label="Gurobi",
    )
    plt.plot(
        mosek_size, mosek_time, "o-", color="firebrick", label="Mosek",
    )
    plt.plot(
        qoco_size, qoco_time, "X-", color="royalblue", label="QOCO",
    )
    plt.plot(
        qoco_custom_size,
        qoco_custom_time,
        "X-",
        color="mediumvioletred",
        label="QOCO Custom",
    )
    plt.yscale("log")
    plt.title("LCvx", usetex=True)

    df_qoco_group_lasso = pd.read_csv("./results/group_lasso/qoco.csv")
    df_qoco_custom_group_lasso = pd.read_csv("./results/group_lasso/qoco_custom.csv")
    df_clarabel_group_lasso = pd.read_csv("./results/group_lasso/clarabel.csv")
    df_mosek_group_lasso = pd.read_csv("./results/group_lasso/mosek.csv")
    df_gurobi_group_lasso = pd.read_csv("./results/group_lasso/gurobi.csv")
    df_ecos_group_lasso = pd.read_csv("./results/group_lasso/ecos.csv")

    qoco_size, qoco_time = get_average_solvetime(df_qoco_group_lasso)
    qoco_custom_size, qoco_custom_time = get_average_solvetime(
        df_qoco_custom_group_lasso
    )
    clarabel_size, clarabel_time = get_average_solvetime(df_clarabel_group_lasso)
    gurobi_size, gurobi_time = get_average_solvetime(df_gurobi_group_lasso)
    mosek_size, mosek_time = get_average_solvetime(df_mosek_group_lasso)
    ecos_size, ecos_time = get_average_solvetime(df_ecos_group_lasso)

    plt.subplot(323)
    plt.plot(
        clarabel_size, clarabel_time, "o-", color="darkviolet", label="Clarabel",
    )
    plt.plot(
        ecos_size, ecos_time, "o-", color="mediumseagreen", label="ECOS",
    )
    plt.plot(
        gurobi_size, gurobi_time, "o-", color="coral", label="Gurobi",
    )
    plt.plot(
        mosek_size, mosek_time, "o-", color="firebrick", label="Mosek",
    )
    plt.plot(
        qoco_size, qoco_time, "X-", color="royalblue", label="QOCO",
    )
    plt.plot(
        qoco_custom_size,
        qoco_custom_time,
        "X-",
        color="mediumvioletred",
        label="QOCO Custom",
    )
    plt.yscale("log")
    plt.title("Group Lasso", usetex=True)

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

    ax = plt.subplot(324)
    pos = ax.get_position()
    xright = pos.x0
    plt.plot(
        clarabel_size, clarabel_time, "o-", color="darkviolet", label="Clarabel",
    )
    plt.plot(
        ecos_size, ecos_time, "o-", color="mediumseagreen", label="ECOS",
    )
    plt.plot(
        gurobi_size, gurobi_time, "o-", color="coral", label="Gurobi",
    )
    plt.plot(
        mosek_size, mosek_time, "o-", color="firebrick", label="Mosek",
    )
    plt.plot(
        qoco_size, qoco_time, "X-", color="royalblue", label="QOCO",
    )
    plt.plot(
        qoco_custom_size,
        qoco_custom_time,
        "X-",
        color="mediumvioletred",
        label="QOCO Custom",
    )
    plt.yscale("log")
    plt.title("Portfolio Optimization", usetex=True)

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
    qoco_custom_size, qoco_custom_time = get_average_solvetime(
        df_qoco_custom_oscillating_masses
    )
    clarabel_size, clarabel_time = get_average_solvetime(df_clarabel_oscillating_masses)
    gurobi_size, gurobi_time = get_average_solvetime(df_gurobi_oscillating_masses)
    mosek_size, mosek_time = get_average_solvetime(df_mosek_oscillating_masses)
    ecos_size, ecos_time = get_average_solvetime(df_ecos_oscillating_masses)
    cvxgen_size, cvxgen_time = get_average_solvetime(df_cvxgen_oscillating_masses)

    ax = plt.subplot(325)
    plt.plot(
        clarabel_size, clarabel_time, "o-", color="darkviolet", label="Clarabel",
    )
    plt.plot(
        cvxgen_size, cvxgen_time, "o-", color="olive", label="CVXGEN",
    )
    plt.plot(
        ecos_size, ecos_time, "o-", color="mediumseagreen", label="ECOS",
    )
    plt.plot(
        gurobi_size, gurobi_time, "o-", color="coral", label="Gurobi",
    )
    plt.plot(
        mosek_size, mosek_time, "o-", color="firebrick", label="Mosek",
    )
    plt.plot(
        qoco_size, qoco_time, "X-", color="royalblue", label="QOCO",
    )
    plt.plot(
        qoco_custom_size,
        qoco_custom_time,
        "X-",
        color="mediumvioletred",
        label="QOCO Custom",
    )
    plt.plot(
        cvxgen_size, cvxgen_time, "o-", color="olive",
    )
    plt.yscale("log")
    plt.title("Oscillating Masses", usetex=True)
    plt.tight_layout()
    pos = ax.get_position()
    ax.set_position([0.5 * (pos.x0 + xright), pos.y0, pos.width, pos.height])
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(handles, labels, loc="center right", bbox_to_anchor=(1.5, 0.5))

    strFile = "plots/benchmark_problems.pdf"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)

    # Plot performance profiles
    df_perf = pd.read_csv("./results/overall/relative_profile.csv")
    plt.figure(dpi=200)
    plt.plot(
        df_perf["tau"].values,
        df_perf["clarabel"].values,
        color="darkviolet",
        label="Clarabel",
    )
    plt.plot(
        df_perf["tau"].values,
        df_perf["ecos"].values,
        color="mediumseagreen",
        label="ECOS",
    )
    plt.plot(
        df_perf["tau"].values, df_perf["gurobi"].values, color="coral", label="Gurobi",
    )
    plt.plot(
        df_perf["tau"].values,
        df_perf["mosek"].values,
        color="firebrick",
        label="Mosek",
    )
    plt.plot(
        df_perf["tau"].values, df_perf["qoco"].values, color="royalblue", label="QOCO",
    )

    plt.legend(loc="lower right")
    plt.ylabel("Ratio of problem solved", usetex=True)
    plt.xlabel("Performance ratio", usetex=True)
    plt.grid()
    plt.xscale("log")
    plt.title("Performance Ratio", usetex=True)
    strFile = "plots/benchmark_problems_relative_profile.pdf"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)

    df_perf = pd.read_csv("./results/overall/absolute_profile.csv")
    plt.figure(dpi=200)
    plt.plot(
        df_perf["tau"].values,
        df_perf["clarabel"].values,
        color="darkviolet",
        label="Clarabel",
    )
    plt.plot(
        df_perf["tau"].values,
        df_perf["ecos"].values,
        color="mediumseagreen",
        label="ECOS",
    )
    plt.plot(
        df_perf["tau"].values, df_perf["gurobi"].values, color="coral", label="Gurobi",
    )
    plt.plot(
        df_perf["tau"].values,
        df_perf["mosek"].values,
        color="firebrick",
        label="Mosek",
    )
    plt.plot(
        df_perf["tau"].values, df_perf["qoco"].values, color="royalblue", label="QOCO",
    )

    plt.legend(loc="lower right")
    plt.ylabel("Fraction of problem solved within t", usetex=True)
    plt.xlabel("Solvetime t [seconds]", usetex=True)
    plt.grid()
    plt.xscale("log")
    plt.title("Solution Time Profile", usetex=True)
    strFile = "plots/benchmark_problems_absolute_profile.pdf"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)

    # Plot performance profiles
    df_perf = pd.read_csv("./results/maros/relative_profile.csv")
    plt.figure(dpi=200)
    plt.plot(
        df_perf["tau"].values,
        df_perf["clarabel"].values,
        color="darkviolet",
        label="Clarabel",
    )
    plt.plot(
        df_perf["tau"].values,
        df_perf["ecos"].values,
        color="mediumseagreen",
        label="ECOS",
    )
    plt.plot(
        df_perf["tau"].values, df_perf["gurobi"].values, color="coral", label="Gurobi",
    )
    plt.plot(
        df_perf["tau"].values,
        df_perf["mosek"].values,
        color="firebrick",
        label="Mosek",
    )
    plt.plot(
        df_perf["tau"].values, df_perf["qoco"].values, color="royalblue", label="QOCO",
    )

    plt.legend(loc="lower right")
    plt.ylabel("Ratio of problem solved", usetex=True)
    plt.xlabel("Performance ratio", usetex=True)
    plt.grid()
    plt.xscale("log")
    plt.title("Performance Ratio", usetex=True)
    strFile = "plots/maros_relative_profile.pdf"
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)

    df_perf = pd.read_csv("./results/maros/absolute_profile.csv")
    plt.figure(dpi=200)
    plt.plot(
        df_perf["tau"].values,
        df_perf["clarabel"].values,
        color="darkviolet",
        label="Clarabel",
    )
    plt.plot(
        df_perf["tau"].values,
        df_perf["ecos"].values,
        color="mediumseagreen",
        label="ECOS",
    )
    plt.plot(
        df_perf["tau"].values, df_perf["gurobi"].values, color="coral", label="Gurobi",
    )
    plt.plot(
        df_perf["tau"].values,
        df_perf["mosek"].values,
        color="firebrick",
        label="Mosek",
    )
    plt.plot(
        df_perf["tau"].values, df_perf["qoco"].values, color="royalblue", label="QOCO",
    )

    plt.legend(loc="lower right")
    plt.ylabel("Fraction of problem solved within t", usetex=True)
    plt.xlabel("Solvetime t [seconds]", usetex=True)
    plt.grid()
    plt.xscale("log")
    plt.title("Solution Time Profile", usetex=True)
    strFile = "plots/maros_absolute_profile.pdf"
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
