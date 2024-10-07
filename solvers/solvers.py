import cvxpy as cp
import qcospy as qcos
from solvers.cvxpy_to_qcos import *
from solvers.run_generated_solver import *
import warnings

def piqp_solve(prob, tol):
    sol = prob.solve(solver=cp.PIQP, eps_abs=tol, eps_rel=tol, eps_duality_gap_abs=tol, eps_duality_gap_rel=tol)
    res = {
        "status": prob.status,
        "setup_time": prob.solver_stats.setup_time,
        "solve_time": prob.solver_stats.solve_time,
        "run_time": float(prob.solver_stats.setup_time or 0) + prob.solver_stats.solve_time,
        "obj": sol,
    }
    return res

def clarabel_solve(prob, tol):
    sol = prob.solve(solver=cp.CLARABEL, tol_gap_abs=tol, tol_gap_rel=tol, tol_feas=tol, verbose=True)
    res = {
        "status": prob.status,
        "setup_time": prob.solver_stats.setup_time,
        "solve_time": prob.solver_stats.solve_time,
        "run_time": float(prob.solver_stats.setup_time or 0) + prob.solver_stats.solve_time,
        "obj": sol,
    }
    return res

def ecos_solve(prob, tol):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    sol = prob.solve(solver=cp.ECOS, abstol=tol, reltol=tol, feastol=tol)
    res = {
        "status": prob.status,
        "setup_time": prob.solver_stats.setup_time,
        "solve_time": prob.solver_stats.solve_time,
        "run_time": float(prob.solver_stats.setup_time or 0) + prob.solver_stats.solve_time,
        "obj": sol,
    }
    return res

def qcos_solve(prob, tol):
    n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
    prob_qcos = qcos.QCOS()
    prob_qcos.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q, abstol=tol, reltol=tol)
    res_qcos = prob_qcos.solve()
    res = {
        "status": res_qcos.status,
        "setup_time": res_qcos.setup_time_sec,
        "solve_time": res_qcos.solve_time_sec,
        "run_time": res_qcos.setup_time_sec + res_qcos.solve_time_sec,
        "obj": res_qcos.obj,
    }
    return res

def qcos_custom_solve(prob, custom_solver_dir, solver_name, regenerate_solver):
    n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
    prob_qcos = qcos.QCOS()
    prob_qcos.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q)
    if regenerate_solver:
        prob_qcos.generate_solver(custom_solver_dir, solver_name)
    codegen_solved, codegen_obj, average_runtime_ms = run_generated_solver(custom_solver_dir+"/"+solver_name)

    status = 'failed'
    if codegen_solved:
        status = 'optimal'

    res = {
        "status": status,
        "setup_time": None,
        "solve_time": average_runtime_ms / 1000,
        "run_time": average_runtime_ms / 1000,
        "obj": codegen_obj,
    }
    return res