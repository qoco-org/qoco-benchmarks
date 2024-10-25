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

    rkf_size = set(df_gurobi_robust_kalman_filter["size"])
    rkf_size = [*rkf_size]
    rkf_size.sort()
    rkf_size_custom = set(df_qoco_custom_robust_kalman_filter["size"])
    rkf_size_custom = [*rkf_size_custom]
    rkf_size_custom.sort()
    rkf_ecos_time = []
    rkf_mosek_time = []
    rkf_gurobi_time = []
    rkf_clarabel_time = []
    rkf_qoco_time = []
    rkf_qoco_custom_time = []

    for size in rkf_size:
        idx = df_gurobi_robust_kalman_filter[df_gurobi_robust_kalman_filter['size'] == size].index
        rkf_ecos_time.append(1000 * np.nanmean(df_ecos_robust_kalman_filter['run_time'][idx]))
        rkf_mosek_time.append(1000 * np.nanmean(df_mosek_robust_kalman_filter['run_time'][idx]))
        rkf_gurobi_time.append(1000 * np.nanmean(df_gurobi_robust_kalman_filter['run_time'][idx]))
        rkf_clarabel_time.append(1000 * np.nanmean(df_clarabel_robust_kalman_filter['run_time'][idx]))
        rkf_qoco_time.append(1000 * np.nanmean(df_qoco_robust_kalman_filter['run_time'][idx]))
    for size in rkf_size_custom:
        idx = df_qoco_custom_robust_kalman_filter[df_qoco_custom_robust_kalman_filter['size'] == size].index
        rkf_qoco_custom_time.append(1000 * np.nanmean(df_qoco_custom_robust_kalman_filter['run_time'][idx]))

    plt.figure()
    plt.plot(
        rkf_size,
        rkf_ecos_time,
        "o-",
        color="green",
        label="ECOS",
    )
    plt.plot(
        rkf_size,
        rkf_mosek_time,
        "o-",
        color="red",
        label="MOSEK",
    )
    plt.plot(
        rkf_size,
        rkf_gurobi_time,
        "o-",
        color="orange",
        label="Gurobi",
    )
    plt.plot(
        rkf_size,
        rkf_clarabel_time,
        "o-",
        color="purple",
        label="Clarabel",
    )
    plt.plot(
        rkf_size,
        rkf_qoco_time,
        "o-",
        color="blue",
        label="QOCO",
    )
    plt.plot(
        rkf_size_custom,
        rkf_qoco_custom_time,
        "o-",
        color="black",
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

    rkf_size = set(df_gurobi_lcvx["size"])
    rkf_size = [*rkf_size]
    rkf_size.sort()
    rkf_size_custom = set(df_qoco_custom_lcvx["size"])
    rkf_size_custom = [*rkf_size_custom]
    rkf_size_custom.sort()
    rkf_ecos_time = []
    rkf_mosek_time = []
    rkf_gurobi_time = []
    rkf_clarabel_time = []
    rkf_qoco_time = []
    rkf_qoco_custom_time = []
    for size in rkf_size:
        idx = df_gurobi_lcvx[df_gurobi_lcvx['size'] == size].index
        rkf_ecos_time.append(1000 * np.nanmean(df_ecos_lcvx['run_time'][idx]))
        rkf_mosek_time.append(1000 * np.nanmean(df_mosek_lcvx['run_time'][idx]))
        rkf_gurobi_time.append(1000 * np.nanmean(df_gurobi_lcvx['run_time'][idx]))
        rkf_clarabel_time.append(1000 * np.nanmean(df_clarabel_lcvx['run_time'][idx]))
        rkf_qoco_time.append(1000 * np.nanmean(df_qoco_lcvx['run_time'][idx]))
    for size in rkf_size_custom:
        idx = df_qoco_custom_lcvx[df_qoco_custom_lcvx['size'] == size].index
        rkf_qoco_custom_time.append(1000 * np.nanmean(df_qoco_custom_lcvx['run_time'][idx]))

    plt.figure()
    plt.plot(
        rkf_size,
        rkf_ecos_time,
        "o-",
        color="green",
        label="ECOS",
    )
    plt.plot(
        rkf_size,
        rkf_mosek_time,
        "o-",
        color="red",
        label="MOSEK",
    )
    plt.plot(
        rkf_size,
        rkf_gurobi_time,
        "o-",
        color="orange",
        label="Gurobi",
    )
    plt.plot(
        rkf_size,
        rkf_clarabel_time,
        "o-",
        color="purple",
        label="Clarabel",
    )
    plt.plot(
        rkf_size,
        rkf_qoco_time,
        "o-",
        color="blue",
        label="QOCO",
    )
    plt.plot(
        rkf_size_custom,
        rkf_qoco_custom_time,
        "o-",
        color="black",
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

    rkf_size = set(df_gurobi_portfolio["size"])
    rkf_size = [*rkf_size]
    rkf_size.sort()
    rkf_size_custom = set(df_qoco_custom_portfolio["size"])
    rkf_size_custom = [*rkf_size_custom]
    rkf_size_custom.sort()
    rkf_ecos_time = []
    rkf_mosek_time = []
    rkf_gurobi_time = []
    rkf_clarabel_time = []
    rkf_qoco_time = []
    rkf_qoco_custom_time = []

    for size in rkf_size:
        idx = df_gurobi_portfolio[df_gurobi_portfolio['size'] == size].index
        rkf_ecos_time.append(1000 * np.nanmean(df_ecos_portfolio['run_time'][idx]))
        rkf_mosek_time.append(1000 * np.nanmean(df_mosek_portfolio['run_time'][idx]))
        rkf_gurobi_time.append(1000 * np.nanmean(df_gurobi_portfolio['run_time'][idx]))
        rkf_clarabel_time.append(1000 * np.nanmean(df_clarabel_portfolio['run_time'][idx]))
        rkf_qoco_time.append(1000 * np.nanmean(df_qoco_portfolio['run_time'][idx]))
    for size in rkf_size_custom:
        idx = df_qoco_custom_portfolio[df_qoco_custom_portfolio['size'] == size].index
        rkf_qoco_custom_time.append(1000 * np.min(df_qoco_custom_portfolio['run_time'][idx]))

    plt.figure()
    plt.plot(
        rkf_size,
        rkf_ecos_time,
        "o-",
        color="green",
        label="ECOS",
    )
    plt.plot(
        rkf_size,
        rkf_mosek_time,
        "o-",
        color="red",
        label="MOSEK",
    )
    plt.plot(
        rkf_size,
        rkf_gurobi_time,
        "o-",
        color="orange",
        label="Gurobi",
    )
    plt.plot(
        rkf_size,
        rkf_clarabel_time,
        "o-",
        color="purple",
        label="Clarabel",
    )
    plt.plot(
        rkf_size,
        rkf_qoco_time,
        "o-",
        color="blue",
        label="QOCO",
    )
    plt.plot(
        rkf_size_custom,
        rkf_qoco_custom_time,
        "o-",
        color="black",
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
    rkf_size = set(df_gurobi_oscillating_masses["size"])
    rkf_size = [*rkf_size]
    rkf_size.sort()
    rkf_size_custom = set(df_qoco_custom_oscillating_masses["size"])
    rkf_size_custom = [*rkf_size_custom]
    rkf_size_custom.sort()
    rkf_size_cvxgen = set(df_cvxgen_oscillating_masses["size"])
    rkf_size_cvxgen = [*rkf_size_cvxgen]
    rkf_size_cvxgen.sort()

    rkf_ecos_time = []
    rkf_mosek_time = []
    rkf_gurobi_time = []
    rkf_clarabel_time = []
    rkf_qoco_time = []
    rkf_qoco_custom_time = []
    rkf_cvxgen_time = []

    for size in rkf_size:
        idx = df_gurobi_oscillating_masses[df_gurobi_oscillating_masses['size'] == size].index
        rkf_ecos_time.append(1000 * np.nanmean(df_ecos_oscillating_masses['run_time'][idx]))
        rkf_mosek_time.append(1000 * np.nanmean(df_mosek_oscillating_masses['run_time'][idx]))
        rkf_gurobi_time.append(1000 * np.nanmean(df_gurobi_oscillating_masses['run_time'][idx]))
        rkf_clarabel_time.append(1000 * np.nanmean(df_clarabel_oscillating_masses['run_time'][idx]))
        rkf_qoco_time.append(1000 * np.nanmean(df_qoco_oscillating_masses['run_time'][idx]))
    for size in rkf_size_custom:
        idx = df_qoco_custom_oscillating_masses[df_qoco_custom_oscillating_masses['size'] == size].index
        rkf_qoco_custom_time.append(1000 * np.nanmean(df_qoco_custom_oscillating_masses['run_time'][idx]))
    for size in rkf_size_cvxgen:
        idx = df_cvxgen_oscillating_masses[df_cvxgen_oscillating_masses['size'] == size].index
        rkf_cvxgen_time.append(1000 * np.nanmean(df_cvxgen_oscillating_masses['run_time'][idx]))

    plt.figure()
    plt.plot(
        rkf_size,
        rkf_ecos_time,
        "o-",
        color="green",
        label="ECOS",
    )
    plt.plot(
        rkf_size,
        rkf_mosek_time,
        "o-",
        color="red",
        label="MOSEK",
    )
    plt.plot(
        rkf_size,
        rkf_gurobi_time,
        "o-",
        color="orange",
        label="Gurobi",
    )
    plt.plot(
        rkf_size,
        rkf_clarabel_time,
        "o-",
        color="purple",
        label="Clarabel",
    )
    plt.plot(
        rkf_size,
        rkf_qoco_time,
        "o-",
        color="blue",
        label="QOCO",
    )
    plt.plot(
        rkf_size_custom,
        rkf_qoco_custom_time,
        "o-",
        color="black",
        label="QOCO Custom",
    )
    plt.plot(
        rkf_size_cvxgen,
        rkf_cvxgen_time,
        "o-",
        color="steelblue",
        label="CVXGEN",
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

    rkf_size = set(df_gurobi_group_lasso["size"])
    rkf_size = [*rkf_size]
    rkf_size.sort()
    # rkf_size_custom = set(df_qoco_custom_group_lasso["size"])
    # rkf_size_custom = [*rkf_size_custom]
    # rkf_size_custom.sort()
    rkf_ecos_time = []
    rkf_mosek_time = []
    rkf_gurobi_time = []
    rkf_clarabel_time = []
    rkf_qoco_time = []
    rkf_qoco_custom_time = []

    for size in rkf_size:
        idx = df_gurobi_group_lasso[df_gurobi_group_lasso['size'] == size].index
        rkf_ecos_time.append(1000 * np.nanmean(df_ecos_group_lasso['run_time'][idx]))
        rkf_mosek_time.append(1000 * np.nanmean(df_mosek_group_lasso['run_time'][idx]))
        rkf_gurobi_time.append(1000 * np.nanmean(df_gurobi_group_lasso['run_time'][idx]))
        rkf_clarabel_time.append(1000 * np.nanmean(df_clarabel_group_lasso['run_time'][idx]))
        rkf_qoco_time.append(1000 * np.nanmean(df_qoco_group_lasso['run_time'][idx]))
    # for size in rkf_size_custom:
    #     idx = df_qoco_custom_group_lasso[df_qoco_custom_group_lasso['size'] == size].index
    #     rkf_qoco_custom_time.append(1000 * np.nanmean(df_qoco_custom_group_lasso['run_time'][idx]))

    plt.figure()
    plt.plot(
        rkf_size,
        rkf_ecos_time,
        "o-",
        color="green",
        label="ECOS",
    )
    plt.plot(
        rkf_size,
        rkf_mosek_time,
        "o-",
        color="red",
        label="MOSEK",
    )
    plt.plot(
        rkf_size,
        rkf_gurobi_time,
        "o-",
        color="orange",
        label="Gurobi",
    )
    plt.plot(
        rkf_size,
        rkf_clarabel_time,
        "o-",
        color="purple",
        label="Clarabel",
    )
    plt.plot(
        rkf_size,
        rkf_qoco_time,
        "o-",
        color="blue",
        label="QOCO",
    )
    # plt.plot(
    #     rkf_size_custom,
    #     rkf_qoco_custom_time,
    #     "o-",
    #     color="black",
    #     label="QOCO Custom",
    # )
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
    assert np.linalg.norm(
        df_gurobi_robust_kalman_filter["obj"].values[0:100]
        - df_qoco_custom_robust_kalman_filter["obj"].values[0:100],
        np.inf,
    ) < 1e-5
    assert np.linalg.norm(
        df_gurobi_lcvx["obj"].values[0:100]
        - df_qoco_custom_lcvx["obj"].values[0:100],
        np.inf,
    ) < 1e-5
    # assert (
    #     np.linalg.norm(
    #         df_gurobi_portfolio["obj"].values[0:100]
    #         - df_qoco_custom_portfolio["obj"].values[0:100],
    #         np.inf,
    #     )
    #     < 1e-5
    # )
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
    # assert (
    #     np.linalg.norm(
    #         df_gurobi_group_lasso["obj"].values[0:100]
    #         - df_qoco_custom_group_lasso["obj"].values[0:100],
    #         np.inf,
    #     )
    #     < 1e-5
    # )

    plt.show()
