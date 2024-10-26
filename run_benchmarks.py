from run_problems.run_lcvx import *
from run_problems.run_robust_kalman_filter import *
from run_problems.run_portfolio import *
from run_problems.run_oscillating_masses import *
from run_problems.run_group_lasso import *
from plotall import plotall

regen_solver = False
ninstances = 20
nruns = 1
# run_lcvx(regen_solver, ninstances, nruns)
# run_robust_kalman_filter(regen_solver, ninstances, nruns)
# run_portfolio(regen_solver, ninstances, nruns)
# run_oscillating_masses(regen_solver, ninstances, nruns)
run_group_lasso(regen_solver, ninstances, nruns)
plotall()
