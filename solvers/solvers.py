import cvxpy as cp
import numpy as np
import qoco
from solvers.cvxpy_to_qoco import *
from solvers.run_generated_solver import *
import warnings


# def piqp_solve(prob, tol):
#     sol = prob.solve(
#         solver=cp.PIQP,
#         eps_abs=tol,
#         eps_rel=tol,
#         eps_duality_gap_abs=tol,
#         eps_duality_gap_rel=tol,
#     )
#     res = {
#         "status": prob.status,
#         "setup_time": prob.solver_stats.setup_time,
#         "solve_time": prob.solver_stats.solve_time,
#         "run_time": float(prob.solver_stats.setup_time or 0)
#         + prob.solver_stats.solve_time,
#         "obj": sol,
#     }
#     assert prob.status == "optimal"
#     return res


def mosek_solve(prob, tol=1e-7, N=100):
    total_setup_time = 0
    total_solve_time = 0
    try:
        for i in range(N):
            sol = prob.solve(solver=cp.MOSEK)
            total_setup_time += float(prob.solver_stats.setup_time or 0)
            total_solve_time += prob.solver_stats.solve_time
        res = {
            "nvar": prob.size_metrics.num_scalar_variables,
            "status": prob.status,
            "setup_time": total_setup_time / N,
            "solve_time": total_solve_time / N,
            "run_time": (total_setup_time + total_solve_time) / N,
            "obj": sol,
        }
    except:
        print("Mosek Failed")
        res = {
            "nvar": prob.size_metrics.num_scalar_variables,
            "status": np.nan,
            "setup_time": np.nan,
            "solve_time": np.nan,
            "run_time": np.nan,
            "obj": np.nan,
        }
    return res


def clarabel_solve(prob, tol=1e-7, N=100):
    total_setup_time = 0
    total_solve_time = 0
    for i in range(N):
        sol = prob.solve(
            solver=cp.CLARABEL, tol_gap_abs=tol, tol_gap_rel=tol, tol_feas=tol
        )
        total_setup_time += float(prob.solver_stats.setup_time or 0)
        total_solve_time += prob.solver_stats.solve_time
    res = {
        "nvar": prob.size_metrics.num_scalar_variables,
        "status": prob.status,
        "setup_time": total_setup_time / N,
        "solve_time": total_solve_time / N,
        "run_time": (total_setup_time + total_solve_time) / N,
        "obj": sol,
    }
    assert prob.status == "optimal"
    return res


def ecos_solve(prob, tol=1e-7, N=100):
    warnings.simplefilter(action="ignore", category=FutureWarning)
    total_setup_time = 0
    total_solve_time = 0
    try:
        for i in range(N):
            sol = prob.solve(solver=cp.ECOS, abstol=tol, reltol=tol, feastol=tol)
            total_setup_time += float(prob.solver_stats.setup_time or 0)
            total_solve_time += prob.solver_stats.solve_time
        res = {
            "nvar": prob.size_metrics.num_scalar_variables,
            "status": prob.status,
            "setup_time": total_setup_time / N,
            "solve_time": total_solve_time / N,
            "run_time": (total_setup_time + total_solve_time) / N,
            "obj": sol,
        }
    except:
        print("ECOS Failed")
        res = {
            "nvar": prob.size_metrics.num_scalar_variables,
            "status": np.nan,
            "setup_time": np.nan,
            "solve_time": np.nan,
            "run_time": np.nan,
            "obj": np.nan,
        }
    return res


def qoco_solve(prob, tol=1e-7, N=100):
    total_setup_time = 0
    total_solve_time = 0
    n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
    prob_qoco = qoco.QOCO()
    prob_qoco.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q, abstol=tol, reltol=tol)

    for i in range(N):
        res_qoco = prob_qoco.solve()
        total_setup_time += float(res_qoco.setup_time_sec or 0)
        total_solve_time += res_qoco.solve_time_sec
    res = {
        "nvar": prob.size_metrics.num_scalar_variables,
        "status": res_qoco.status,
        "setup_time": total_setup_time / N,
        "solve_time": total_solve_time / N,
        "run_time": (total_setup_time + total_solve_time) / N,
        "obj": res_qoco.obj,
    }
    assert res_qoco.status == "QOCO_SOLVED"
    return res


def qoco_custom_solve(prob, custom_solver_dir, solver_name, regenerate_solver):
    n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
    prob_qoco = qoco.QOCO()
    prob_qoco.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q)
    if regenerate_solver:
        prob_qoco.generate_solver(custom_solver_dir, solver_name)
    codegen_solved, codegen_obj, average_runtime_ms = run_generated_solver(
        custom_solver_dir + "/" + solver_name
    )

    assert codegen_solved

    status = "failed"
    if codegen_solved == 1:
        status = "optimal"

    res = {
        "nvar": prob.size_metrics.num_scalar_variables,
        "status": status,
        "setup_time": None,
        "solve_time": average_runtime_ms / 1000,
        "run_time": average_runtime_ms / 1000,
        "obj": codegen_obj,
    }
    return res
