import os, shutil
import pandas as pd
import numpy as np

SOLUTION_PRESENT = ["QOCO_SOLVED", "solved", "Solved", "Status.PIQP_SOLVED", "optimal"]


# Creates directory ./results/overall and for each solver generates a .csv that concatinates the results from all the problems solved. Need this to compute overall performance plots.
def get_overall_performance(solvers):
    results = "./results"
    os.makedirs("./results/overall", exist_ok=True)

    # Loop over all solvers.
    for solver in solvers:
        overall_df = pd.DataFrame()
        # Loop over all problems
        for item in os.listdir(results):
            if item == "overall":
                continue
            item_path = os.path.join(results, item)
            df = pd.read_csv(os.path.join(item_path, solver + ".csv"))
            overall_df = pd.concat([overall_df, df], ignore_index=True)
        overall_df.to_csv(os.path.join("./results/overall", solver + ".csv"))


# Function is from osqp_benchmarks (https://github.com/osqp/osqp_benchmarks/blob/master/utils/benchmark.py#L61)
def compute_performance_profiles(solvers, dir):
    t = {}
    status = {}
    for solver in solvers:
        path = os.path.join(dir, solver + ".csv")
        with open(path, "rb") as f:
            df = pd.read_csv(path)

            n_prob = len(df)
            t[solver] = df["run_time"].values
            status[solver] = df["status"].values

            # Set max time for solvers that did not succeed
            for idx in range(n_prob):
                if status[solver][idx] not in SOLUTION_PRESENT:
                    t[solver][idx] = 1e3

    # Dictionary of relative times for each solver/problem
    r = {}
    for s in solvers:
        r[s] = np.zeros(n_prob)

    # Iterate over all problems to find btest timing between solvers
    for p in range(n_prob):
        # Get minimum time
        min_time = np.min([t[s][p] for s in solvers])

        # Normalize t for minimum time
        for s in solvers:
            r[s][p] = t[s][p] / min_time

    # Compute curve for all solvers
    n_tau = 1000
    tau_vec = np.logspace(0, 4, n_tau)
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
    performance_profiles_file = os.path.join(dir, "performance_profiles.csv")
    df_performance_profiles.to_csv(performance_profiles_file, index=False)
