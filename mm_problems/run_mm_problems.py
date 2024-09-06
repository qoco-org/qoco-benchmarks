import scipy.io
from pathlib import Path
import qcospy as qcos
from parse_mm import *
from cvxpy_to_qcos import convert

directory = Path("mm_problems/MAT_Files")
for file_path in directory.iterdir():
    if file_path.is_file():
        mat = scipy.io.loadmat(file_path)
        print(file_path)
        if len(mat["lb"]) > 200:
            continue
        n, m, p, P, c, A, b, G, h, l, nsoc, q = parse_mm(mat)
        prob_qcos = qcos.QCOS()
        prob_qcos.setup(n, m, p, P, c, A, b, G, h, l, nsoc, q, verbose=1)
        res = prob_qcos.solve()
