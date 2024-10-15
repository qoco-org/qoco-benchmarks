% csolve  Solves a custom quadratic program very rapidly.
%
% [vars, status] = csolve(params, settings)
%
% solves the convex optimization problem
%
%   minimize(quad_form(x_0, Q) + quad_form(u_0, R) + quad_form(x_1, Q) + quad_form(u_1, R) + quad_form(x_2, Q) + quad_form(u_2, R) + quad_form(x_3, Q) + quad_form(u_3, R) + quad_form(x_4, Q) + quad_form(u_4, R) + quad_form(x_5, Q) + quad_form(u_5, R) + quad_form(x_6, Q) + quad_form(u_6, R) + quad_form(x_7, Q) + quad_form(u_7, R) + quad_form(x_8, Q) + quad_form(u_8, R) + quad_form(x_9, Q) + quad_form(u_9, R) + quad_form(x_10, Q) + quad_form(u_10, R) + quad_form(x_11, Q) + quad_form(u_11, R) + quad_form(x_12, Q) + quad_form(u_12, R) + quad_form(x_13, Q) + quad_form(u_13, R) + quad_form(x_14, Q) + quad_form(u_14, R) + quad_form(x_15, Q) + quad_form(u_15, R) + quad_form(x_16, Q) + quad_form(u_16, R) + quad_form(x_17, Q) + quad_form(u_17, R) + quad_form(x_18, Q) + quad_form(u_18, R) + quad_form(x_19, Q) + quad_form(u_19, R) + quad_form(x_20, Q))
%   subject to
%     x_1 == A*x_0 + B*u_0
%     x_2 == A*x_1 + B*u_1
%     x_3 == A*x_2 + B*u_2
%     x_4 == A*x_3 + B*u_3
%     x_5 == A*x_4 + B*u_4
%     x_6 == A*x_5 + B*u_5
%     x_7 == A*x_6 + B*u_6
%     x_8 == A*x_7 + B*u_7
%     x_9 == A*x_8 + B*u_8
%     x_10 == A*x_9 + B*u_9
%     x_11 == A*x_10 + B*u_10
%     x_12 == A*x_11 + B*u_11
%     x_13 == A*x_12 + B*u_12
%     x_14 == A*x_13 + B*u_13
%     x_15 == A*x_14 + B*u_14
%     x_16 == A*x_15 + B*u_15
%     x_17 == A*x_16 + B*u_16
%     x_18 == A*x_17 + B*u_17
%     x_19 == A*x_18 + B*u_18
%     x_20 == A*x_19 + B*u_19
%     abs(u_0) <= u_max
%     abs(u_1) <= u_max
%     abs(u_2) <= u_max
%     abs(u_3) <= u_max
%     abs(u_4) <= u_max
%     abs(u_5) <= u_max
%     abs(u_6) <= u_max
%     abs(u_7) <= u_max
%     abs(u_8) <= u_max
%     abs(u_9) <= u_max
%     abs(u_10) <= u_max
%     abs(u_11) <= u_max
%     abs(u_12) <= u_max
%     abs(u_13) <= u_max
%     abs(u_14) <= u_max
%     abs(u_15) <= u_max
%     abs(u_16) <= u_max
%     abs(u_17) <= u_max
%     abs(u_18) <= u_max
%     abs(u_19) <= u_max
%     abs(x_1) <= x_max
%     abs(x_2) <= x_max
%     abs(x_3) <= x_max
%     abs(x_4) <= x_max
%     abs(x_5) <= x_max
%     abs(x_6) <= x_max
%     abs(x_7) <= x_max
%     abs(x_8) <= x_max
%     abs(x_9) <= x_max
%     abs(x_10) <= x_max
%     abs(x_11) <= x_max
%     abs(x_12) <= x_max
%     abs(x_13) <= x_max
%     abs(x_14) <= x_max
%     abs(x_15) <= x_max
%     abs(x_16) <= x_max
%     abs(x_17) <= x_max
%     abs(x_18) <= x_max
%     abs(x_19) <= x_max
%
% with variables
%      u_0   4 x 1
%      u_1   4 x 1
%      u_2   4 x 1
%      u_3   4 x 1
%      u_4   4 x 1
%      u_5   4 x 1
%      u_6   4 x 1
%      u_7   4 x 1
%      u_8   4 x 1
%      u_9   4 x 1
%     u_10   4 x 1
%     u_11   4 x 1
%     u_12   4 x 1
%     u_13   4 x 1
%     u_14   4 x 1
%     u_15   4 x 1
%     u_16   4 x 1
%     u_17   4 x 1
%     u_18   4 x 1
%     u_19   4 x 1
%      x_1   8 x 1
%      x_2   8 x 1
%      x_3   8 x 1
%      x_4   8 x 1
%      x_5   8 x 1
%      x_6   8 x 1
%      x_7   8 x 1
%      x_8   8 x 1
%      x_9   8 x 1
%     x_10   8 x 1
%     x_11   8 x 1
%     x_12   8 x 1
%     x_13   8 x 1
%     x_14   8 x 1
%     x_15   8 x 1
%     x_16   8 x 1
%     x_17   8 x 1
%     x_18   8 x 1
%     x_19   8 x 1
%     x_20   8 x 1
%
% and parameters
%        A   8 x 8
%        B   8 x 4
%        Q   8 x 8    PSD, diagonal
%        R   4 x 4    PSD, diagonal
%    u_max   1 x 1    positive
%      x_0   8 x 1
%    x_max   1 x 1    positive
%
% Note:
%   - Check status.converged, which will be 1 if optimization succeeded.
%   - You don't have to specify settings if you don't want to.
%   - To hide output, use settings.verbose = 0.
%   - To change iterations, use settings.max_iters = 20.
%   - You may wish to compare with cvxsolve to check the solver is correct.
%
% Specify params.A, ..., params.x_max, then run
%   [vars, status] = csolve(params, settings)
% Produced by CVXGEN, 2024-10-15 11:02:31 -0400.
% CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com.
% The code in this file is Copyright (C) 2006-2017 Jacob Mattingley.
% CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial
% applications without prior written permission from Jacob Mattingley.

% Filename: csolve.m.
% Description: Help file for the Matlab solver interface.
