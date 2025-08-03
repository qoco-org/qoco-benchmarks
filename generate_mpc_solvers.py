import scipy.io
from pathlib import Path
from mm_problems.mm_opt import *
from solvers.solvers import *
from mpc.construct_mpc_problem import construct_mpc_problem

import qocogen
from solvers.cvxpy_to_qoco import convert

directory = Path("mpc/data")
for file_path in directory.iterdir():
    if file_path.is_file():
        mat = scipy.io.loadmat(file_path, struct_as_record=False, squeeze_me=True)
        prob = construct_mpc_problem(mat)
        problem_name = file_path.stem
        name = problem_name.removeprefix("matFiles_")
        print(name)
        n, m, p, P, c, A, b, G, h, l, nsoc, q = convert(prob)
        qocogen.generate_solver(
            n, m, p, P, c, A, b, G, h, l, nsoc, q, "./generated_solvers", name
        )
