# QOCO Benchmarks

This repository was used to generated the numerical results in the paper titled [QOCO: A Quadratic Objective Conic Optimizer with Custom Solver Generation](https://arxiv.org/abs/2503.12658).

To run benchmarks, first create a python 3.12 virtual environment and install the requirements with

```
pip install -r requirements.txt
```


Before running the benchmark problems, the user must generate the cvxgen solvers using the problem files in the `cvxgen/problems/` directory and place them in a directory called `generated_solvers/` within the `cvxgen/` directory (If you have already extracted the `cvxgen.tar.gz` archive file, this step can be skipped).

To run the benchmark problems, create a directory titled `generated_solvers/` in the root of the repository then run

```
python generate_benchmark_solvers.py && python run_benchmarks.py && python analyze_benchmarks.py
```

To run the MPC problems, run

```
python generate_mpc_solvers.py && python run_mpc.py && python analyze_mpc.py
```


To run the Maros-Meszaros problems and generate plots run

```
python run_maros.py && python analyze_maros.py
```

To run the SuiteSparse problems and generate plots run

```
python run_suitesparse.py && python analyze_suitesparse.py
```


To generate all solvers and run all benchmarks and generate all plots, run

```
./run_all.sh
```

## Citing
```
@article{chari2026qoco,
  title = {QOCO: a quadratic objective conic optimizer with custom solver generation},
  author = {Chari, Govind M. and A\c{c}ıkmeşe, Beh\c{c}et},
  journal = {Mathematical Programming Computation},
  issn = {1867-2957},
  url = {http://dx.doi.org/10.1007/s12532-026-00311-8},
  doi = {10.1007/s12532-026-00311-8},
  publisher = {Springer Science and Business Media LLC},
  year = {2026},
  month = mar,
}
```
