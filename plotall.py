from matplotlib import pyplot as plt
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
    df_qoco_custom_robust_kalman_filter["nvar"],
    1000 * df_qoco_custom_robust_kalman_filter["run_time"],
    "o-",
    color="black",
    label="QOCO Custom",
)
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
plt.legend(loc="lower right")
plt.xlabel("Number of Variables")
plt.ylabel("Solvetime [milliseconds]")
plt.yscale("log")
plt.savefig("plots/robust_kalman_filter.pdf")

df_qoco_lcvx = pd.read_csv("./results/lcvx/qoco.csv")
df_qoco_custom_lcvx = pd.read_csv("./results/lcvx/qoco_custom.csv")
df_clarabel_lcvx = pd.read_csv("./results/lcvx/clarabel.csv")
df_mosek_lcvx = pd.read_csv("./results/lcvx/mosek.csv")
df_ecos_lcvx = pd.read_csv("./results/lcvx/ecos.csv")

plt.figure()
plt.plot(
    df_qoco_custom_lcvx["nvar"],
    1000 * df_qoco_custom_lcvx["run_time"],
    "o-",
    color="black",
    label="QOCO Custom",
)
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

plt.legend(loc="lower right")
plt.xlabel("Number of Variables")
plt.ylabel("Solvetime [milliseconds]")
plt.yscale("log")
plt.savefig("plots/lcvx.pdf")
# plt.show()
