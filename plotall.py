from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
from matplotlib import rc

plt.rcParams.update({"text.usetex": True, "font.family": "Helvetica"})

df_qoco_robust_kalman_filter = pd.read_csv("./results/robust_kalman_filter/qoco.csv")
df_qoco_custom_robust_kalman_filter = pd.read_csv(
    "./results/robust_kalman_filter/qoco_custom.csv"
)
df_clarabel_robust_kalman_filter = pd.read_csv(
    "./results/robust_kalman_filter/clarabel.csv"
)
df_mosek_robust_kalman_filter = pd.read_csv("./results/robust_kalman_filter/mosek.csv")
df_ecos_robust_kalman_filter = pd.read_csv("./results/robust_kalman_filter/ecos.csv")

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
strFile = "plots/robust_kalman_filter.pdf"
if os.path.isfile(strFile):
    os.remove(strFile)
plt.savefig(strFile)
df_qoco_lcvx = pd.read_csv("./results/lcvx/qoco.csv")
df_qoco_custom_lcvx = pd.read_csv("./results/lcvx/qoco_custom.csv")
df_clarabel_lcvx = pd.read_csv("./results/lcvx/clarabel.csv")
df_mosek_lcvx = pd.read_csv("./results/lcvx/mosek.csv")
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
failed_idx = np.where(df_mosek_lcvx["status"].values != "optimal")
plt.scatter(
    df_mosek_lcvx["nvar"].values[failed_idx],
    top * np.ones(len(failed_idx[0])),
    color="red",
    marker="x",
)
# top = plt.ylim()[1]
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
strFile = "plots/lcvx.pdf"
if os.path.isfile(strFile):
    os.remove(strFile)
plt.savefig(strFile)
# plt.show()
