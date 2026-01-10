import os, shutil
import pandas as pd
import numpy as np
import re

SOLUTION_PRESENT = ["QOCO_SOLVED", "solved", "Solved", "Status.PIQP_SOLVED", "optimal"]


# Creates directory ./results/overall and for each solver generates a .csv that concatanates the results from all the problems solved.
# Need this to compute overall performance plots.
def get_overall_performance(solvers):
    if "qoco_custom" in solvers:
        dir = "./results/overall_custom"
        nprob = 100
    else:
        dir = "./results/overall"
        nprob = 200

    os.makedirs(dir, exist_ok=True)

    # Loop over all solvers.
    for s in solvers:
        overall_df = pd.DataFrame()
        # Loop over all problems
        for item in os.listdir("./results"):
            if item == "overall" or item == "overall_custom" or item == "maros" or item == "suitesparse" or item == "mpc":
                continue
            item_path = os.path.join("./results", item)
            df = pd.read_csv(os.path.join(item_path, s + ".csv"))[0:nprob]
            overall_df = pd.concat([overall_df, df], ignore_index=True)
        overall_df.to_csv(os.path.join(dir, s + ".csv"))


# Function is from osqp_benchmarks (https://github.com/osqp/osqp_benchmarks/blob/master/utils/benchmark.py#L61)
# Computes relative performannce profile and saves data to .csv in dir.
def compute_relative_profile(solvers, tmax, dir, xrange=(0, 2)):
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
                    t[s][idx] = tmax

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
    tau_vec = np.logspace(xrange[0], xrange[1], n_tau)
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
def compute_absolute_profile(solvers, tmax, dir, xrange=(-4.3, 1)):
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
                    t[s][idx] = tmax

    # Compute curve for all solvers
    n_tau = 1000
    tau_vec = np.logspace(xrange[0], xrange[1], n_tau)
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
def compute_shifted_geometric_mean(solvers, tmax, dir, name):
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
                    t[s][idx] = tmax

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


def compute_shifted_geometric_mean_custom(solvers, tmax, dir, name):
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
                    t[s][idx] = tmax

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
    f.write("\\begin{tabular}{lcccccc}\n")
    f.write("  \hline\n")
    f.write(
        "    & \\textbf{QOCO Custom}   & \\textbf{QOCO} & \\textbf{Clarabel} & \\textbf{ECOS} & \\textbf{Gurobi} & \\textbf{Mosek} \\\ \\hline\n"
    )
    f.write(
        "  Shifted GM & %.1f & %.1f & %.1f & %.1f & %.1f & %.1f \\\ \n"
        % (
            rs["qoco_custom"],
            rs["qoco"],
            rs["clarabel"],
            rs["ecos"],
            rs["gurobi"],
            rs["mosek"],
        )
    )
    f.write(
        "  Failure Rate (\%%) & %.1f & %.1f & %.1f & %.1f & %.1f & %.1f \\\ \hline \n"
        % (
            fail["qoco_custom"],
            fail["qoco"],
            fail["clarabel"],
            fail["ecos"],
            fail["gurobi"],
            fail["mosek"],
        )
    )
    f.write("\end{tabular}\n")
    f.close()


def make_table(solvers, dir, name, caption):
    os.makedirs("./plots", exist_ok=True)
    out_path = os.path.join("./plots", name + "_detail_table.tex")

    # Load all solver CSVs once and index by problem name
    dfs = {}
    for s in solvers:
        df = pd.read_csv(os.path.join(dir, s + ".csv"))
        df = df.set_index("Unnamed: 0")
        dfs[s] = df

    # Use the first solver to define sorted problem order
    base_df = dfs[solvers[0]].sort_index()
    prob_names = base_df.index.tolist()
    prob_sizes = base_df["size"].tolist()

    ns = len(solvers)

    with open(out_path, "w") as f:
        f.write("\\scriptsize\n")
        f.write("\\begin{longtable}{lc||%s||%s||}\n" % (ns * "c", ns * "c"))
        f.write("\\captionsetup{labelfont=bf}\n")
        f.write("\\caption{\\bf %s} \\\\ \n" % caption)
        f.write(
            " & & \\multicolumn{%i}{c||}{\\underline{Iterations}} "
            "& \\multicolumn{%i}{c||}{\\underline{Solver Runtime (s)}}"
            "\\\\[2ex]\n" % (ns, ns)
        )

        f.write("Problem & Size ")
        for s in solvers:
            f.write("& \\textsc{%s} " % re.sub(r"_", r"\_", s))
        for s in solvers:
            f.write("& \\textsc{%s} " % re.sub(r"_", r"\_", s))
        f.write("\\\\[1ex]\n")
        f.write("\\hline\n")
        f.write("\\endhead\n")

        # Iterate over problems
        for name, size in zip(prob_names, prob_sizes):
            min_iter = np.inf
            min_time = np.inf
            iter_winners = []
            time_winner = None

            # Determine winners
            for s in solvers:
                df = dfs[s]
                if name not in df.index:
                    continue

                data = df.loc[name]

                if (
                    data["status"] in SOLUTION_PRESENT
                    and "iters" in data
                    and not np.isnan(data["iters"])
                ):
                    it = int(data["iters"])
                    if it < min_iter:
                        min_iter = it
                        iter_winners = [s]
                    elif it == min_iter:
                        iter_winners.append(s)

                if data["status"] in SOLUTION_PRESENT:
                    if data["run_time"] < min_time:
                        min_time = data["run_time"]
                        time_winner = s

            # Write row header
            tex_name = re.sub(r"_", r"\_", name)
            f.write("\\textsc{%s} & %i " % (tex_name, size))

            # Write iteration columns
            for s in solvers:
                df = dfs[s]
                if name not in df.index:
                    f.write("& -")
                    continue

                data = df.loc[name]
                if (
                    data["status"] not in SOLUTION_PRESENT
                    or "iters" not in data
                    or np.isnan(data["iters"])
                ):
                    f.write("& -")
                else:
                    f.write("& ")
                    if s in iter_winners:
                        f.write(" \\winner ")
                    f.write("%i " % int(data["iters"]))

            # Write runtime columns
            for s in solvers:
                df = dfs[s]
                if name not in df.index:
                    f.write("& -")
                    continue

                data = df.loc[name]
                if data["status"] not in SOLUTION_PRESENT:
                    f.write("& -")
                else:
                    f.write("& ")
                    if s == time_winner:
                        f.write(" \\winner ")
                    f.write("%.5f " % data["run_time"])

            f.write("\\\\\n")

        f.write("\\end{longtable}\n")
