import os, shutil
import pandas as pd
import numpy as np

SOLUTION_PRESENT = ["QOCO_SOLVED", "solved", "Solved", "Status.PIQP_SOLVED", "optimal"]

timelimit = 20


# Creates directory ./results/overall and for each solver generates a .csv that concatanates the results from all the problems solved.
# Need this to compute overall performance plots.
def get_overall_performance(solvers):
    results = "./results"
    os.makedirs("./results/overall", exist_ok=True)

    # Loop over all solvers.
    for s in solvers:
        overall_df = pd.DataFrame()
        # Loop over all problems
        for item in os.listdir(results):
            if item == "overall":
                continue
            item_path = os.path.join(results, item)
            df = pd.read_csv(os.path.join(item_path, s + ".csv"))
            overall_df = pd.concat([overall_df, df], ignore_index=True)
        overall_df.to_csv(os.path.join("./results/overall", s + ".csv"))


# Function is from osqp_benchmarks (https://github.com/osqp/osqp_benchmarks/blob/master/utils/benchmark.py#L61)
# Computes relative performannce profile and saves data to .csv in dir.
def compute_relative_profile(solvers, dir):
    t = {}
    status = {}
    for s in solvers:
        path = os.path.join(dir, s + ".csv")
        with open(path, "rb") as f:
            df = pd.read_csv(path)

            n_prob = len(df)
            t[s] = df["run_time"].values
            status[s] = df["status"].values

            # Set max time for solvers that did not succeed
            for idx in range(n_prob):
                if status[s][idx] not in SOLUTION_PRESENT:
                    t[s][idx] = timelimit

    # Dictionary of relative times for each solver/problem
    r = {}
    for s in solvers:
        r[s] = np.zeros(n_prob)

    # Iterate over all problems to find best timing between solvers
    for p in range(n_prob):
        # Get minimum time
        min_time = np.min([t[s][p] for s in solvers])

        # Normalize t for minimum time
        for s in solvers:
            r[s][p] = t[s][p] / min_time

    # Compute curve for all solvers
    n_tau = 1000
    tau_vec = np.logspace(0, 2, n_tau)
    rho = {"tau": tau_vec}

    for s in solvers:
        rho[s] = np.zeros(n_tau)
        for tau_idx in range(n_tau):
            count_problems = 0  # Count number of problems with t[p, s] <= tau
            for p in range(n_prob):
                if r[s][p] <= tau_vec[tau_idx]:
                    count_problems += 1
            rho[s][tau_idx] = count_problems / n_prob

    # Store final pandas dataframe
    df_performance_profiles = pd.DataFrame(rho)
    performance_profiles_file = os.path.join(dir, "relative_profile.csv")
    df_performance_profiles.to_csv(performance_profiles_file, index=False)


# Computes absolute performannce profile and saves data to .csv in dir.
def compute_absolute_profile(solvers, dir):
    t = {}
    status = {}
    for s in solvers:
        path = os.path.join(dir, s + ".csv")
        with open(path, "rb") as f:
            df = pd.read_csv(path)

            n_prob = len(df)
            t[s] = df["run_time"].values
            status[s] = df["status"].values

            # Set max time for solvers that did not succeed
            for idx in range(n_prob):
                if status[s][idx] not in SOLUTION_PRESENT:
                    t[s][idx] = timelimit

    # Compute curve for all solvers
    n_tau = 1000
    tau_vec = np.logspace(-4, 1, n_tau)
    rho = {"tau": tau_vec}

    for s in solvers:
        rho[s] = np.zeros(n_tau)
        for tau_idx in range(n_tau):
            count_problems = 0  # Count number of problems with t[p, s] <= tau
            for p in range(n_prob):
                if t[s][p] <= tau_vec[tau_idx]:
                    count_problems += 1
            rho[s][tau_idx] = count_problems / n_prob

    # Store final pandas dataframe
    df_performance_profiles = pd.DataFrame(rho)
    performance_profiles_file = os.path.join(dir, "absolute_profile.csv")
    df_performance_profiles.to_csv(performance_profiles_file, index=False)


# Computes sgm and writes .tex table to plots directory.
def compute_shifted_geometric_mean(solvers, dir, name):
    t = {}
    status = {}
    fail = {}
    for s in solvers:
        fail[s] = 0
        path = os.path.join(dir, s + ".csv")
        with open(path, "rb") as f:
            df = pd.read_csv(path)

            n_prob = len(df)
            t[s] = df["run_time"].values
            status[s] = df["status"].values

            # Set max time for solvers that did not succeed
            for idx in range(n_prob):
                if status[s][idx] not in SOLUTION_PRESENT:
                    fail[s] += 1
                    t[s][idx] = timelimit

    rs = {}
    for s in solvers:
        rs[s] = 1
        for p in range(n_prob):
            rs[s] *= 1 + t[s][p]
        rs[s] = (rs[s] ** (1 / n_prob)) - 1

    mings = np.min([rs[s] for s in solvers])
    for s in solvers:
        rs[s] /= mings
        fail[s] *= 100 / n_prob
    f = open(os.path.join("./plots", name + "_sgm.tex"), "w")
    f.write("\\begin{tabular}{lccccc}\n")
    f.write("  \hline\n")
    f.write(
        "   & \\textbf{QOCO} & \\textbf{Clarabel} & \\textbf{ECOS} & \\textbf{Gurobi} & \\textbf{Mosek} \\\ \\hline\n"
    )
    f.write(
        "  Shifted GM & %.1f & %.1f & %.1f & %.1f & %.1f \\\ \n"
        % (rs["qoco"], rs["clarabel"], rs["ecos"], rs["gurobi"], rs["mosek"])
    )
    f.write(
        "  Failure Rate (\%%) & %.1f & %.1f & %.1f & %.1f & %.1f \\\ \hline \n"
        % (fail["qoco"], fail["clarabel"], fail["ecos"], fail["gurobi"], fail["mosek"])
    )
    f.write("\end{tabular}\n")
    f.close()
