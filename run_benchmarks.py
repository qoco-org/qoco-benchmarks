from run_lcvx import *
from run_robust_kalman_filter import *
from run_portfolio import *
from run_oscillating_masses import *
from run_group_lasso import *
from plotall import plotall

regen_solver = False
# run_lcvx(regen_solver)
# run_robust_kalman_filter(regen_solver)
# run_portfolio(regen_solver)
run_oscillating_masses(regen_solver)
# run_group_lasso(regen_solver)
plotall()
