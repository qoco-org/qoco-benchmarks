import os
import struct
import numpy as np


def run_generated_qoco(solver_dir, nruns, P, A, G, c, b, h):
    # Write new runtest.c that has helper function to update vector problem data.
    if os.path.isfile(solver_dir + "/runtest.c"):
        os.remove(solver_dir + "/runtest.c")

    f = create_qoco_runtest(solver_dir, nruns, P, A, G, c, b, h)

    # Run the solver.
    os.system("cd " + solver_dir + " && mkdir build")
    os.system(
        "cd "
        + solver_dir
        + "/build && cmake -DQOCO_CUSTOM_BUILD_TYPE:STR=Release .. && make -j5 && ./runtest && cd ../.."
    )
    with open(solver_dir + "/build/result.bin", "rb") as file:
        solved = struct.unpack("B", file.read(1))[0]
        iters = struct.unpack("I", file.read(4))[0]
        obj = struct.unpack("d", file.read(8))[0]
        runtime_sec = struct.unpack("d", file.read(8))[0]
    return solved, iters, obj, runtime_sec


def run_generated_cvxgen(solver_dir, x0, Q, R, A, B, umax, xmax, nruns):
    create_cvxgen_runtest(solver_dir, nruns, x0, Q, R, A, B, umax, xmax)
    os.system("cd " + solver_dir + " && make -j5 && ./testsolver")
    with open(solver_dir + "/result.bin", "rb") as file:
        solved = struct.unpack("B", file.read(1))[0]
        obj = struct.unpack("d", file.read(8))[0]
        runtime_sec = struct.unpack("d", file.read(8))[0]
    return solved, obj, runtime_sec


def create_cvxgen_runtest(solver_dir, nruns, x0, Q, R, A, B, umax, xmax):
    if os.path.isfile(solver_dir + "/testsolver.c"):
        os.remove(solver_dir + "/testsolver.c")

    f = open(solver_dir + "/testsolver.c", "a")
    f.write("#include <stdio.h>\n")
    f.write("#include <time.h>\n")
    f.write('#include "solver.h"\n')
    f.write("#define MIN(a,b) (((a)<(b))?(a):(b))\n\n")
    f.write("Vars vars;\n")
    f.write("Params params;\n")
    f.write("Workspace work;\n")
    f.write("Settings settings;\n")
    f.write("int main(int argc, char **argv) {\n")
    f.write("  set_defaults();\n")
    f.write("   setup_indexing();\n")
    f.write("   settings.verbose = 0;\n")
    f.write("   settings.resid_tol = 1e-7;\n")
    f.write("   settings.eps = 1e-7;\n")
    f.write("   double N = %i;\n" % nruns)
    f.write("   double solve_time_sec = 1e10;\n")
    f.write("   for (int i = 0; i < N; ++i) {\n")
    f.write("       struct timespec start, end;\n")
    f.write("       clock_gettime(CLOCK_MONOTONIC, &start);\n")
    f.write("       load_default_data();\n")
    f.write("       solve();\n")
    f.write("       clock_gettime(CLOCK_MONOTONIC, &end);\n")
    f.write(
        "       double elapsed_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;\n"
    )
    f.write("       solve_time_sec = MIN(solve_time_sec, elapsed_time);\n")
    f.write("   }\n")
    f.write('   printf("\\nSolvetime: %.9f ms", 1e3 * solve_time_sec);\n')
    f.write('   FILE *file = fopen("result.bin", "wb");\n')
    f.write("   fwrite(&work.converged, sizeof(unsigned char), 1, file);\n")
    f.write("   fwrite(&work.optval, sizeof(double), 1, file);\n")
    f.write("   fwrite(&solve_time_sec, sizeof(double), 1, file);\n")
    f.write("   fclose(file);\n")
    f.write('   printf("\\nobj: %.17g", work.optval);\n')
    f.write("}\n\n")

    f.write("void load_default_data() {\n")
    n, m = B.shape
    for i in range(n):
        f.write("   params.x_0[%i] = %.17g;\n" % (i, x0[i]))
    for i in range(n):
        f.write("   params.Q[%i] = %.17g;\n" % (i, Q[i, i]))
    for i in range(m):
        f.write("   params.R[%i] = %.17g;\n" % (i, R[i, i]))
    for j in range(n):
        for i in range(n):
            f.write("   params.A[%i] = %.17g;\n" % (j * n + i, A[i, j]))
    for j in range(m):
        for i in range(n):
            f.write("   params.B[%i] = %.17g;\n" % (j * n + i, B[i, j]))
    f.write("   params.u_max[0] = %.17g;\n" % (umax))
    f.write("   params.x_max[0] = %.17g;\n" % (xmax))
    f.write("}\n")
    f.close()


def create_qoco_runtest(solver_dir, nruns, P, A, G, c, b, h):
    f = open(solver_dir + "/runtest.c", "a")
    f.write("#include <stdio.h>\n")
    f.write("#include <time.h>\n")
    f.write('#include "qoco_custom.h"\n\n')

    f.write("void update_data(Workspace* work) {\n")

    Pnnz = P.nnz if P is not None else 0
    for i in range(Pnnz):
        f.write("   work->P[%i] = %.17g;\n" % (i, P.data[i]))
    for i in range(A.nnz):
        f.write("   work->A[%i] = %.17g;\n" % (i, A.data[i]))
    for i in range(G.nnz):
        f.write("   work->G[%i] = %.17g;\n" % (i, G.data[i]))
    for i in range(len(c)):
        f.write("   work->c[%i] = %.17g;\n" % (i, c[i]))
    for i in range(len(b)):
        f.write("   work->b[%i] = %.17g;\n" % (i, b[i]))
    for i in range(len(h)):
        f.write("   work->h[%i] = %.17g;\n" % (i, h[i]))
    f.write("}\n\n")

    f.write("int main() {\n")
    f.write("   Workspace work;\n")
    f.write("   set_default_settings(&work);\n")
    f.write("   work.settings.verbose = 0;\n")
    f.write("   double N = %i;\n" % nruns)
    f.write("   double solve_time_sec = 1e10;\n")
    f.write("   for (int i = 0; i < N; ++i) {\n")
    f.write("       struct timespec start, end;\n")
    f.write("       load_data(&work);\n")
    f.write("       clock_gettime(CLOCK_MONOTONIC, &start);\n")
    f.write("       update_data(&work);\n")
    f.write("       qoco_custom_solve(&work);\n")
    f.write("       clock_gettime(CLOCK_MONOTONIC, &end);\n")
    f.write(
        "       double elapsed_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;\n"
    )
    f.write("       solve_time_sec = qoco_min(solve_time_sec, elapsed_time);\n")
    f.write("   }\n")
    f.write('   printf("\\nSolvetime: %.9f ms", 1e3 * solve_time_sec);\n')
    f.write('   FILE *file = fopen("result.bin", "wb");\n')
    f.write("   fwrite(&work.sol.status, sizeof(unsigned char), 1, file);\n")
    f.write("   fwrite(&work.sol.iters, sizeof(int), 1, file);\n")
    f.write("   fwrite(&work.sol.obj, sizeof(double), 1, file);\n")
    f.write("   fwrite(&solve_time_sec, sizeof(double), 1, file);\n")
    f.write("   fclose(file);\n")
    f.write('   printf("\\nobj: %.17g", work.sol.obj);\n')
    f.write("}\n\n")
