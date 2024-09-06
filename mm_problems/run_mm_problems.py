import scipy.io
from pathlib import Path
import qcospy as qcos
import osqp
import clarabel
from parse_mm import *
from types import SimpleNamespace
import pickle

solve_dict = {}
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

        # n, m, p, P, c, A, b, G, h, l, nsoc, q = parse_mm_qcos(mat)
        # prob_qcos = qcos.QCOS()
        # prob_qcos.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q, verbose=0)
        # res_qcos = prob_qcos.solve()

        # P, q, A, l, u = parse_mm_osqp(mat)
        # m = osqp.OSQP()
        # m.setup(P=P, q=q, A=A, l=l, u=u, eps_abs=1e-7, eps_rel=1e-7, verbose=True)
        # res = m.solve()
        # solve_dict[problem_name] = SimpleNamespace(
        #     status=res.info.status,
        #     setup_time_sec=res.info.setup_time,
        #     solve_time_sec=res.info.solve_time,
        #     pres=res.info.pri_res,
        #     dres=res.info.dua_res,
        #     obj=res.info.obj_val
        # )

        settings = clarabel.DefaultSettings()
        settings.tol_gap_abs = 1e-7
        settings.tol_gap_rel = 1e-7
        settings.tol_feas = 1e-7
        # settings.tol_infeas_abs = 1e-7
        # settings.tol_infeas_rel = 1e-7

        P, q, A, b, cones = parse_mm_clarabel(mat)
        solver = clarabel.DefaultSolver(P,q,A,b,cones,settings)
        res = solver.solve()
        solve_dict[problem_name] = SimpleNamespace(
            status=str(res.status),
            solve_time_sec=res.solve_time,
            obj=res.obj_val
        )

with open("mm_clarabel_40k.pkl", "wb") as f:
    pickle.dump(solve_dict, f)
