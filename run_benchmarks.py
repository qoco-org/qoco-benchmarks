from run_lcvx import *
from run_robust_kalman_filter import *
from run_portfolio import *
from plotall import plotall

regen_solver = False
run_lcvx(regen_solver)
run_robust_kalman_filter(regen_solver)
run_portfolio(regen_solver)
plotall()
