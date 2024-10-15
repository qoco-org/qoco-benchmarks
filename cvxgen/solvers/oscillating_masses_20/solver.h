/* Produced by CVXGEN, 2024-10-15 11:03:01 -0400.  */
/* CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com. */
/* The code in this file is Copyright (C) 2006-2017 Jacob Mattingley. */
/* CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial */
/* applications without prior written permission from Jacob Mattingley. */

/* Filename: solver.h. */
/* Description: Header file with relevant definitions. */
#ifndef SOLVER_H
#define SOLVER_H
/* Uncomment the next line to remove all library dependencies. */
/*#define ZERO_LIBRARY_MODE */
#ifdef MATLAB_MEX_FILE
/* Matlab functions. MATLAB_MEX_FILE will be defined by the mex compiler. */
/* If you are not using the mex compiler, this functionality will not intrude, */
/* as it will be completely disabled at compile-time. */
#include "mex.h"
#else
#ifndef ZERO_LIBRARY_MODE
#include <stdio.h>
#endif
#endif
/* Space must be allocated somewhere (testsolver.c, csolve.c or your own */
/* program) for the global variables vars, params, work and settings. */
/* At the bottom of this file, they are externed. */
#ifndef ZERO_LIBRARY_MODE
#include <math.h>
#define pm(A, m, n) printmatrix(#A, A, m, n, 1)
#endif
typedef struct Params_t {
  double x_0[8];
  double Q[8];
  double R[4];
  double A[64];
  double B[32];
  double u_max[1];
  double x_max[1];
  double *x[1];
} Params;
typedef struct Vars_t {
  double *u_0; /* 4 rows. */
  double *x_1; /* 8 rows. */
  double *u_1; /* 4 rows. */
  double *x_2; /* 8 rows. */
  double *u_2; /* 4 rows. */
  double *x_3; /* 8 rows. */
  double *u_3; /* 4 rows. */
  double *x_4; /* 8 rows. */
  double *u_4; /* 4 rows. */
  double *x_5; /* 8 rows. */
  double *u_5; /* 4 rows. */
  double *x_6; /* 8 rows. */
  double *u_6; /* 4 rows. */
  double *x_7; /* 8 rows. */
  double *u_7; /* 4 rows. */
  double *x_8; /* 8 rows. */
  double *u_8; /* 4 rows. */
  double *x_9; /* 8 rows. */
  double *u_9; /* 4 rows. */
  double *x_10; /* 8 rows. */
  double *u_10; /* 4 rows. */
  double *x_11; /* 8 rows. */
  double *u_11; /* 4 rows. */
  double *x_12; /* 8 rows. */
  double *u_12; /* 4 rows. */
  double *x_13; /* 8 rows. */
  double *u_13; /* 4 rows. */
  double *x_14; /* 8 rows. */
  double *u_14; /* 4 rows. */
  double *x_15; /* 8 rows. */
  double *u_15; /* 4 rows. */
  double *x_16; /* 8 rows. */
  double *u_16; /* 4 rows. */
  double *x_17; /* 8 rows. */
  double *u_17; /* 4 rows. */
  double *x_18; /* 8 rows. */
  double *u_18; /* 4 rows. */
  double *x_19; /* 8 rows. */
  double *u_19; /* 4 rows. */
  double *x_20; /* 8 rows. */
  double *t_01; /* 4 rows. */
  double *t_02; /* 4 rows. */
  double *t_03; /* 4 rows. */
  double *t_04; /* 4 rows. */
  double *t_05; /* 4 rows. */
  double *t_06; /* 4 rows. */
  double *t_07; /* 4 rows. */
  double *t_08; /* 4 rows. */
  double *t_09; /* 4 rows. */
  double *t_10; /* 4 rows. */
  double *t_11; /* 4 rows. */
  double *t_12; /* 4 rows. */
  double *t_13; /* 4 rows. */
  double *t_14; /* 4 rows. */
  double *t_15; /* 4 rows. */
  double *t_16; /* 4 rows. */
  double *t_17; /* 4 rows. */
  double *t_18; /* 4 rows. */
  double *t_19; /* 4 rows. */
  double *t_20; /* 4 rows. */
  double *t_21; /* 8 rows. */
  double *t_22; /* 8 rows. */
  double *t_23; /* 8 rows. */
  double *t_24; /* 8 rows. */
  double *t_25; /* 8 rows. */
  double *t_26; /* 8 rows. */
  double *t_27; /* 8 rows. */
  double *t_28; /* 8 rows. */
  double *t_29; /* 8 rows. */
  double *t_30; /* 8 rows. */
  double *t_31; /* 8 rows. */
  double *t_32; /* 8 rows. */
  double *t_33; /* 8 rows. */
  double *t_34; /* 8 rows. */
  double *t_35; /* 8 rows. */
  double *t_36; /* 8 rows. */
  double *t_37; /* 8 rows. */
  double *t_38; /* 8 rows. */
  double *t_39; /* 8 rows. */
  double *u[20];
  double *x[21];
} Vars;
typedef struct Workspace_t {
  double h[696];
  double s_inv[696];
  double s_inv_z[696];
  double b[160];
  double q[472];
  double rhs[2024];
  double x[2024];
  double *s;
  double *z;
  double *y;
  double lhs_aff[2024];
  double lhs_cc[2024];
  double buffer[2024];
  double buffer2[2024];
  double KKT[5504];
  double L[5854];
  double d[2024];
  double v[2024];
  double d_inv[2024];
  double gap;
  double optval;
  double ineq_resid_squared;
  double eq_resid_squared;
  double block_33[1];
  /* Pre-op symbols. */
  double quad_645199597568[1];
  int converged;
} Workspace;
typedef struct Settings_t {
  double resid_tol;
  double eps;
  int max_iters;
  int refine_steps;
  int better_start;
  /* Better start obviates the need for s_init and z_init. */
  double s_init;
  double z_init;
  int verbose;
  /* Show extra details of the iterative refinement steps. */
  int verbose_refinement;
  int debug;
  /* For regularization. Minimum value of abs(D_ii) in the kkt D factor. */
  double kkt_reg;
} Settings;
extern Vars vars;
extern Params params;
extern Workspace work;
extern Settings settings;
/* Function definitions in ldl.c: */
void ldl_solve(double *target, double *var);
void ldl_factor(void);
double check_factorization(void);
void matrix_multiply(double *result, double *source);
double check_residual(double *target, double *multiplicand);
void fill_KKT(void);

/* Function definitions in matrix_support.c: */
void multbymA(double *lhs, double *rhs);
void multbymAT(double *lhs, double *rhs);
void multbymG(double *lhs, double *rhs);
void multbymGT(double *lhs, double *rhs);
void multbyP(double *lhs, double *rhs);
void fillq(void);
void fillh(void);
void fillb(void);
void pre_ops(void);

/* Function definitions in solver.c: */
double eval_gap(void);
void set_defaults(void);
void setup_pointers(void);
void setup_indexed_params(void);
void setup_indexed_optvars(void);
void setup_indexing(void);
void set_start(void);
double eval_objv(void);
void fillrhs_aff(void);
void fillrhs_cc(void);
void refine(double *target, double *var);
double calc_ineq_resid_squared(void);
double calc_eq_resid_squared(void);
void better_start(void);
void fillrhs_start(void);
long solve(void);

/* Function definitions in testsolver.c: */
int main(int argc, char **argv);
void load_default_data(void);

/* Function definitions in util.c: */
void tic(void);
float toc(void);
float tocq(void);
void printmatrix(char *name, double *A, int m, int n, int sparse);
double unif(double lower, double upper);
float ran1(long*idum, int reset);
float randn_internal(long *idum, int reset);
double randn(void);
void reset_rand(void);

#endif
