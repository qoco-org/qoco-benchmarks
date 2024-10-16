import cvxpy as cp
from scipy import sparse

def get_problem_size(prob):
    data, _, _ = prob.get_problem_data(cp.CLARABEL)
    nnzA = data["A"].nnz
    nnzP = 0
    if "P" in data.keys():
        nnzP = sparse.triu(data["P"], format="csc").nnz
    return nnzP + nnzA