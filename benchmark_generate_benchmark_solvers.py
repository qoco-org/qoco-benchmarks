import os
import csv
import time
import numpy as np
import qocogen

from solvers.cvxpy_to_qoco import convert
from solvers.problem_size import get_problem_size
from problems.portfolio import portfolio
from problems.group_lasso import group_lasso
from problems.lcvx import lcvx
from problems.oscillating_masses import oscillating_masses
from problems.robust_kalman_filter import robust_kalman_filter

# -----------------------------
# Configuration
# -----------------------------
generated_dir = "./benchmark_generate_dir"
EXCLUDE_FILES = {"runtest.c"}

PROBLEM = {
    "portfolio": portfolio,
    "group_lasso": group_lasso,
    "lcvx": lcvx,
    "oscillating_masses": oscillating_masses,
    "robust_kalman_filter": robust_kalman_filter,
}

# -----------------------------
# Size utilities
# -----------------------------
def get_code_size_kb(root):
    total_bytes = 0
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname in EXCLUDE_FILES:
                continue
            if fname.endswith((".c", ".h")):
                fpath = os.path.join(dirpath, fname)
                if os.path.isfile(fpath):
                    total_bytes += os.path.getsize(fpath)
    return total_bytes / 1024.0


def get_so_size_kb(project_dir):
    so_path = os.path.join(project_dir, "build", "libqoco_custom.so")
    if os.path.isfile(so_path):
        return os.path.getsize(so_path) / 1024.0
    return None


# -----------------------------
# Benchmark driver
# -----------------------------
def benchmark_generate(Nlist, problem_name):
    np.random.seed(123)
    rows = []

    for N in Nlist:
        solver_name = f"{problem_name}_N_{N}"
        solver_dir = os.path.join(generated_dir, solver_name)

        # ---- build problem ----
        prob = PROBLEM[problem_name](N)
        if problem_name == "oscillating_masses":
            prob = prob[0]

        n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)

        # ---- codegen timing ----
        t0 = time.perf_counter()
        qocogen.generate_solver(
            n, m, p, P, c, A, b, G, h, l, nsoc, q,
            generated_dir, solver_name
        )
        codegen_time = time.perf_counter() - t0

        # ---- compile timing ----
        t0 = time.perf_counter()
        os.system(f"cd {solver_dir} && mkdir -p build")
        os.system(
            f"cd {solver_dir}/build && "
            "cmake -DQOCO_CUSTOM_BUILD_TYPE:STR=Release .. && "
            "make -j$(nproc)"
        )
        compile_time = time.perf_counter() - t0

        # ---- size measurements ----
        code_size_kb = get_code_size_kb(solver_dir)
        lib_size_kb = get_so_size_kb(solver_dir)

        rows.append({
            "name": solver_name,
            "size": get_problem_size(prob),
            "codegen_time_s": round(codegen_time, 1),
            "compile_time_s": round(compile_time, 1),
            "code_size_kb": round(code_size_kb),
            "binary_size_kb": round(lib_size_kb) if lib_size_kb else "",
        })

    return rows


# -----------------------------
# Main experiment
# -----------------------------
if __name__ == "__main__":
    os.makedirs(generated_dir, exist_ok=True)

    all_rows = []

    Ngl = [1, 2, 3, 4, 5]
    Nport = [2, 4, 6, 8, 10]
    Nlcvx = [15, 50, 75, 100, 125]
    Nrkf = [25, 50, 75, 125, 175]
    Nom = [8, 20, 32, 44, 56]

    all_rows += benchmark_generate(Ngl, "group_lasso")
    all_rows += benchmark_generate(Nport, "portfolio")
    all_rows += benchmark_generate(Nlcvx, "lcvx")
    all_rows += benchmark_generate(Nrkf, "robust_kalman_filter")
    all_rows += benchmark_generate(Nom, "oscillating_masses")

    # ---- write CSV ----
    output_csv = "benchmark_generate_benchmark_results.csv"
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name",
                "size",
                "codegen_time_s",
                "compile_time_s",
                "code_size_kb",
                "binary_size_kb",
            ],
        )
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Wrote results to {output_csv}")
