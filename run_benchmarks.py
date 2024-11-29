from run_problems.run_lcvx import *
from run_problems.run_robust_kalman_filter import *
from run_problems.run_portfolio import *
from run_problems.run_oscillating_masses import *
from run_problems.run_group_lasso import *
from plotall import plotall
from postprocess import *
from utils import *

ninstances = 20
nruns = 100
run_lcvx(ninstances, nruns)
run_robust_kalman_filter(ninstances, nruns)
run_portfolio(ninstances, nruns)
run_oscillating_masses(ninstances, nruns)
run_group_lasso(ninstances, nruns)

tmax = 10

solvers = ["clarabel", "ecos", "gurobi", "mosek", "qoco"]
get_overall_performance(solvers)
compute_relative_profile(solvers, tmax, "./results/overall")
compute_absolute_profile(solvers, tmax, "./results/overall")
compute_shifted_geometric_mean(solvers, tmax, "./results/overall", "benchmark")

solvers = ["clarabel", "ecos", "gurobi", "mosek", "qoco", "qoco_custom"]
get_overall_performance(solvers)
compute_relative_profile(solvers, tmax, "./results/overall_custom")
compute_absolute_profile(solvers, tmax, "./results/overall_custom")
compute_shifted_geometric_mean_custom(
    solvers, tmax, "./results/overall_custom", "benchmark_custom"
)
plotall()
export_figures()
