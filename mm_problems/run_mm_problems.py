import scipy.io
from pathlib import Path
import qcospy as qcos
import osqp
import clarabel
import piqp
from parse_mm import *
from types import SimpleNamespace
import pickle

solve_dict_qcos = {}
solve_dict_osqp = {}
solve_dict_clarabel = {}
solve_dict_piqp = {}
directory = Path("mm_problems/MAT_Files")
nump = 0
for file_path in directory.iterdir():
    nump += 1
    if file_path.is_file():
        mat = scipy.io.loadmat(file_path)
        problem_name = file_path.stem
        print(file_path)
        if len(mat["lb"]) > 40000:
            continue

        n, m, p, P, c, A, b, G, h, l, nsoc, q = parse_mm_qcos(mat)
        G = G if m > 0 else None
        h = h if m > 0 else None
        A = A if p > 0 else None
        b = b if p > 0 else None
        prob_qcos = qcos.QCOS()
        prob_qcos.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q, verbose=0)
        res_qcos = prob_qcos.solve()
        solve_dict_qcos[problem_name] = res_qcos

        P, q, A, l, u = parse_mm_osqp(mat)
        m = osqp.OSQP()
        m.setup(P=P, q=q, A=A, l=l, u=u, eps_abs=1e-7, eps_rel=1e-7, verbose=False)
        res_osqp = m.solve()
        solve_dict_osqp[problem_name] = SimpleNamespace(
            status=res_osqp.info.status,
            setup_time_sec=res_osqp.info.setup_time,
            solve_time_sec=res_osqp.info.solve_time,
            pres=res_osqp.info.pri_res,
            dres=res_osqp.info.dua_res,
            obj=res_osqp.info.obj_val,
        )

        settings = clarabel.DefaultSettings()
        settings.tol_gap_abs = 1e-7
        settings.tol_gap_rel = 1e-7
        settings.tol_feas = 1e-7
        settings.verbose = False

        P, q, A, b, cones = parse_mm_clarabel(mat)
        solver = clarabel.DefaultSolver(P, q, A, b, cones, settings)
        res_clarabel = solver.solve()
        solve_dict_clarabel[problem_name] = SimpleNamespace(
            status=str(res_clarabel.status),
            solve_time_sec=res_clarabel.solve_time,
            obj=res_clarabel.obj_val,
        )

        P, c, A, b, G, h, x_lb, x_ub = parse_mm_piqp(mat)
        solver = piqp.SparseSolver()
        solver.settings.compute_timings = True
        solver.settings.eps_abs = 1e-7
        solver.settings.eps_rel = 1e-7
        solver.settings.eps_duality_gap_abs = 1e-7
        solver.settings.eps_duality_gap_rel = 1e-7

        solver.setup(P, c, A, b, G, h, x_lb, x_ub)
        status = solver.solve()
        solve_dict_piqp[problem_name] = SimpleNamespace(
            status=str(status),
            solve_time_sec=solver.result.info.run_time,
            obj=solver.result.info.primal_obj,
        )


with open("mm_qcos_40k.pkl", "wb") as f:
    pickle.dump(solve_dict_qcos, f)
with open("mm_osqp_40k.pkl", "wb") as f:
    pickle.dump(solve_dict_osqp, f)
with open("mm_clarabel_40k.pkl", "wb") as f:
    pickle.dump(solve_dict_clarabel, f)
with open("mm_piqp_40k.pkl", "wb") as f:
    pickle.dump(solve_dict_piqp, f)
