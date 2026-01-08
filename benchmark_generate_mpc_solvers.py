import os
import csv
import time
import qocogen
import scipy.io
from pathlib import Path
from solvers.solvers import *
from mpc.construct_mpc_problem import construct_mpc_problem


# -----------------------------
# Configuration
# -----------------------------
generated_dir = "./mpc-generated-solvers"
EXCLUDE_FILES = {"runtest.c"}

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
def benchmark_generate():
    rows = []
    directory = Path("mpc/data")
    i = 0
    for file_path in directory.iterdir():
        if file_path.is_file():
            mat = scipy.io.loadmat(file_path, struct_as_record=False, squeeze_me=True)
            prob = construct_mpc_problem(mat)
            problem_name = file_path.stem
            name = problem_name.removeprefix("matFiles_")
            solver_dir = os.path.join(generated_dir, name)

            print(name)
            n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)

            t0 = time.perf_counter()
            qocogen.generate_solver(
                n, m, p, P, c, A, b, G, h, l, nsoc, q,
                generated_dir, name
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
                "name": name,
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

    all_rows = benchmark_generate()

    # ---- write CSV ----
    output_csv = "benchmark_generate_mpc.csv"
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
