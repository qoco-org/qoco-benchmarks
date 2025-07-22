import cvxpy as cp
import numpy as np
import qoco
import gurobipy
from solvers.cvxpy_to_qoco import *
from solvers.run_generated_solver import *
from solvers.problem_size import get_problem_size
import warnings
import signal


MAX_TIME = 1200
VERBOSE = False


class TimeoutException(Exception):  # Custom exception class
    pass


def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException


def gurobi_solve(prob, tol=1e-7, N=10):
    setup_time = np.inf
    solve_time = np.inf
    env = gurobipy.Env()
    env.setParam("OutputFlag", False)
    env.setParam("BarConvTol", tol)
    env.setParam("BarQCPConvTol", tol)
    env.setParam("FeasibilityTol", tol)
    env.setParam("OptimalityTol", tol)
    try:
        for i in range(N):
            sol = prob.solve(verbose=VERBOSE, solver=cp.GUROBI, env=env)
            setup_time = np.minimum(prob.solver_stats.setup_time or 0, setup_time)
            solve_time = np.minimum(prob.solver_stats.solve_time, solve_time)
        if prob.status == "optimal":
            res = {
                "size": get_problem_size(prob),
                "status": prob.status,
                "setup_time": setup_time,
                "solve_time": solve_time,
                "run_time": setup_time + solve_time,
                "obj": sol,
                "iters": prob.solver_stats.num_iters,
            }
        else:
            res = {
                "size": get_problem_size(prob),
                "status": prob.status,
                "setup_time": np.nan,
                "solve_time": np.nan,
                "run_time": np.nan,
                "obj": np.nan,
                "iters": np.nan,
            }
    except:
        res = {
            "size": get_problem_size(prob),
            "status": np.nan,
            "setup_time": np.nan,
            "solve_time": np.nan,
            "run_time": np.nan,
            "obj": np.nan,
            "iters": np.nan,
        }
    return res


def mosek_solve(prob, tol=1e-7, N=10):
    setup_time = np.inf
    solve_time = np.inf
    try:
        for i in range(N):
            sol = prob.solve(
                verbose=VERBOSE,
                solver=cp.MOSEK,
                mosek_params={
                    "MSK_DPAR_INTPNT_CO_TOL_PFEAS": tol,
                    "MSK_DPAR_INTPNT_CO_TOL_DFEAS": tol,
                    "MSK_DPAR_INTPNT_CO_TOL_REL_GAP": tol,
                    "MSK_DPAR_INTPNT_CO_TOL_MU_RED": tol,
                    "MSK_DPAR_OPTIMIZER_MAX_TIME": MAX_TIME,
                },
            )
            setup_time = np.minimum(prob.solver_stats.setup_time or 0.0, setup_time)
            solve_time = np.minimum(prob.solver_stats.solve_time, solve_time)

        if prob.status == "optimal":
            res = {
                "size": get_problem_size(prob),
                "status": prob.status,
                "setup_time": setup_time,
                "solve_time": solve_time,
                "run_time": setup_time + solve_time,
                "obj": sol,
                "iters": prob.solver_stats.num_iters,
            }
        else:
            res = {
                "size": get_problem_size(prob),
                "status": prob.status,
                "setup_time": np.nan,
                "solve_time": np.nan,
                "run_time": np.nan,
                "obj": np.nan,
                "iters": np.nan,
            }
    except:
        res = {
            "size": get_problem_size(prob),
            "status": np.nan,
            "setup_time": np.nan,
            "solve_time": np.nan,
            "run_time": np.nan,
            "obj": np.nan,
            "iters": np.nan,
        }
    return res


def clarabel_solve(prob, tol=1e-7, N=10):
    setup_time = np.inf
    solve_time = np.inf
    try:
        for i in range(N):
            sol = prob.solve(
                verbose=VERBOSE,
                solver=cp.CLARABEL,
                tol_gap_abs=tol,
                tol_gap_rel=tol,
                tol_feas=tol,
            )
            setup_time = np.minimum(prob.solver_stats.setup_time or 0.0, setup_time)
            solve_time = np.minimum(prob.solver_stats.solve_time, solve_time)

        if prob.status == "optimal":
            res = {
                "size": get_problem_size(prob),
                "status": prob.status,
                "setup_time": setup_time,
                "solve_time": solve_time,
                "run_time": setup_time + solve_time,
                "obj": sol,
                "iters": prob.solver_stats.num_iters,
            }
        else:
            res = {
                "size": get_problem_size(prob),
                "status": prob.status,
                "setup_time": np.nan,
                "solve_time": np.nan,
                "run_time": np.nan,
                "obj": np.nan,
                "iters": np.nan,
            }
    except:
        res = {
            "size": get_problem_size(prob),
            "status": np.nan,
            "setup_time": np.nan,
            "solve_time": np.nan,
            "run_time": np.nan,
            "obj": np.nan,
            "iters": np.nan,
        }
    return res


def ecos_solve(prob, tol=1e-7, N=10):
    warnings.simplefilter(action="ignore", category=FutureWarning)
    signal.signal(signal.SIGALRM, timeout_handler)
    setup_time = np.inf
    solve_time = np.inf
    try:
        for i in range(N):
            signal.alarm(MAX_TIME)
            sol = prob.solve(
                verbose=VERBOSE,
                solver=cp.ECOS,
                abstol=tol,
                reltol=tol,
                feastol=tol,
            )
            setup_time = np.minimum(prob.solver_stats.setup_time or 0, setup_time)
            solve_time = np.minimum(prob.solver_stats.solve_time, solve_time)
        if prob.status == "optimal":
            res = {
                "size": get_problem_size(prob),
                "status": prob.status,
                "setup_time": setup_time,
                "solve_time": solve_time,
                "run_time": setup_time + solve_time,
                "obj": sol,
                "iters": prob.solver_stats.num_iters,
            }
        else:
            res = {
                "size": get_problem_size(prob),
                "status": prob.status,
                "setup_time": np.nan,
                "solve_time": np.nan,
                "run_time": np.nan,
                "obj": np.nan,
                "iters": np.nan,
            }
    except:
        res = {
            "size": get_problem_size(prob),
            "status": np.nan,
            "setup_time": np.nan,
            "solve_time": np.nan,
            "run_time": np.nan,
            "obj": np.nan,
            "iters": np.nan,
        }
    else:
        signal.alarm(0)
    return res


def qoco_solve(prob, tol=1e-7, N=10):
    setup_time = np.inf
    solve_time = np.inf
    n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)

    G = G if m > 0 else None
    h = h if m > 0 else None
    A = A if p > 0 else None
    b = b if p > 0 else None

    prob_qoco = qoco.QOCO()
    prob_qoco.setup(
        n,
        m,
        p,
        P,
        c,
        A,
        b,
        G,
        h,
        l,
        nsoc,
        q,
        abstol=tol,
        reltol=tol,
        verbose=VERBOSE,
    )

    for i in range(N):
        res_qoco = prob_qoco.solve()
        setup_time = np.minimum(res_qoco.setup_time_sec or 0, setup_time)
        solve_time = np.minimum(res_qoco.solve_time_sec, solve_time)
    if res_qoco.status == "QOCO_SOLVED":
        res = {
            "size": get_problem_size(prob),
            "status": res_qoco.status,
            "setup_time": setup_time,
            "solve_time": solve_time,
            "run_time": setup_time + solve_time,
            "obj": res_qoco.obj,
            "iters": res_qoco.iters,
        }
    else:
        res = {
            "size": get_problem_size(prob),
            "status": res_qoco.status,
            "setup_time": np.nan,
            "solve_time": np.nan,
            "run_time": np.nan,
            "obj": np.nan,
            "iters": np.nan,
        }
    return res


def qoco_custom_solve(prob, custom_solver_dir, solver_name, nruns):
    n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
    prob_qoco = qoco.QOCO()
    prob_qoco.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q)
    codegen_solved, codegen_iters, codegen_obj, runtime_sec = run_generated_qoco(
        custom_solver_dir + "/" + solver_name, nruns, P, A, G, c, b, h
    )

    if codegen_solved == 1:
        res = {
            "size": get_problem_size(prob),
            "status": "optimal",
            "setup_time": None,
            "solve_time": runtime_sec,
            "run_time": runtime_sec,
            "obj": codegen_obj,
            "iters": codegen_iters,
        }
    else:
        res = {
            "size": get_problem_size(prob),
            "status": "failed",
            "setup_time": None,
            "solve_time": np.nan,
            "run_time": np.nan,
            "obj": np.nan,
            "iters": np.nan,
        }
    return res
