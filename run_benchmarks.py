from run_lcvx import *
from run_robust_kalman_filter import *
from plotall import plotall

regen_solver = False
run_lcvx(regen_solver)
run_robust_kalman_filter(regen_solver)
plotall()
