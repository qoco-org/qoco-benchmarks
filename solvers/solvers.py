import cvxpy as cp
import numpy as np
import qoco
import gurobipy
from solvers.cvxpy_to_qoco import *
from solvers.run_generated_solver import *
import warnings


def gurobi_solve(prob, tol=1e-7, N=100):
    setup_time = np.inf
    solve_time = np.inf
    env = gurobipy.Env()
    env.setParam("BarConvTol", tol)
    env.setParam("BarQCPConvTol", tol)
    env.setParam("FeasibilityTol", tol)
    env.setParam("OptimalityTol", tol)
    env.setParam("Presolve", 0)
    try:
        for i in range(N):
            sol = prob.solve(solver=cp.GUROBI, env=env)
            setup_time = np.minimum(prob.solver_stats.setup_time or 0, setup_time)
            solve_time = np.minimum(prob.solver_stats.solve_time, solve_time)
        res = {
            "nvar": prob.size_metrics.num_scalar_variables,
            "status": prob.status,
            "setup_time": setup_time,
            "solve_time": solve_time,
            "run_time": setup_time + solve_time,
            "obj": sol,
        }
    except:
        print("Gurobi Failed")
        res = {
            "nvar": prob.size_metrics.num_scalar_variables,
            "status": np.nan,
            "setup_time": np.nan,
            "solve_time": np.nan,
            "run_time": np.nan,
            "obj": np.nan,
        }
    return res


def mosek_solve(prob, tol=1e-7, N=100):
    setup_time = np.inf
    solve_time = np.inf
    try:
        for i in range(N):
            sol = prob.solve(
                solver=cp.MOSEK,
                mosek_params={
                    "MSK_DPAR_INTPNT_CO_TOL_PFEAS": tol,
                    "MSK_DPAR_INTPNT_CO_TOL_DFEAS": tol,
                    "MSK_DPAR_INTPNT_CO_TOL_REL_GAP": tol,
                    "MSK_DPAR_INTPNT_CO_TOL_MU_RED": tol,
                    "MSK_IPAR_PRESOLVE_USE": 0,
                },
            )
            setup_time = np.minimum(prob.solver_stats.setup_time or 0, setup_time)
            solve_time = np.minimum(prob.solver_stats.solve_time, solve_time)
        res = {
            "nvar": prob.size_metrics.num_scalar_variables,
            "status": prob.status,
            "setup_time": setup_time,
            "solve_time": solve_time,
            "run_time": setup_time + solve_time,
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
    setup_time = np.inf
    solve_time = np.inf
    for i in range(N):
        sol = prob.solve(
            solver=cp.CLARABEL, tol_gap_abs=tol, tol_gap_rel=tol, tol_feas=tol
        )
        setup_time = np.minimum(prob.solver_stats.setup_time or 0.0, setup_time)
        solve_time = np.minimum(prob.solver_stats.solve_time, solve_time)
    res = {
        "nvar": prob.size_metrics.num_scalar_variables,
        "status": prob.status,
        "setup_time": setup_time,
        "solve_time": solve_time,
        "run_time": setup_time + solve_time,
        "obj": sol,
    }
    assert prob.status == "optimal"
    return res


def ecos_solve(prob, tol=1e-7, N=100):
    warnings.simplefilter(action="ignore", category=FutureWarning)
    setup_time = np.inf
    solve_time = np.inf
    try:
        for i in range(N):
            sol = prob.solve(
                solver=cp.ECOS,
                abstol=tol,
                reltol=tol,
                feastol=tol,
            )
            setup_time = np.minimum(prob.solver_stats.setup_time or 0, setup_time)
            solve_time = np.minimum(prob.solver_stats.solve_time, solve_time)
        if prob.status == "optimal":
            res = {
                "nvar": prob.size_metrics.num_scalar_variables,
                "status": prob.status,
                "setup_time": setup_time,
                "solve_time": solve_time,
                "run_time": setup_time + solve_time,
                "obj": sol,
            }
        else:
            res = {
                "nvar": prob.size_metrics.num_scalar_variables,
                "status": np.nan,
                "setup_time": np.nan,
                "solve_time": np.nan,
                "run_time": np.nan,
                "obj": np.nan,
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
    setup_time = np.inf
    solve_time = np.inf
    n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
    prob_qoco = qoco.QOCO()
    prob_qoco.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q, abstol=tol, reltol=tol)

    for i in range(N):
        res_qoco = prob_qoco.solve()
        setup_time = np.minimum(res_qoco.setup_time_sec or 0, setup_time)
        solve_time = np.minimum(res_qoco.solve_time_sec, solve_time)
    res = {
        "nvar": prob.size_metrics.num_scalar_variables,
        "status": res_qoco.status,
        "setup_time": setup_time,
        "solve_time": solve_time,
        "run_time": setup_time + solve_time,
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
    codegen_solved, codegen_obj, runtime_sec = run_generated_solver(
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
        "solve_time": runtime_sec,
        "run_time": runtime_sec,
        "obj": codegen_obj,
    }
    return res
