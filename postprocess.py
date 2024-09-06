import pickle
import os


# Modified from osqp_benchmarks
def compute_performance_profiles(solvers):
    t = {}
    for solver in solvers:
        path = os.path.join(".", "mm_" + solver + "_40k.pkl")
        with open(path, "rb") as f:
            data = pickle.load(f)
            n_prob = len(data.keys())

            t[solver] = []
            for keys in data:
                t[solver].append(data["solve_time_sec"])

            breakpoint()
