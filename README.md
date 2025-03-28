# QOCO Benchmarks

This repository was used to generated the numerical results in the paper titled "Custom Solver Generation for Quadratic Objective Second-Order Cone Programs"

To run benchmarks, first create a python virtual environment and install the requirements with

```
pip install -r requirements.txt
```


To run the Maros-Meszaros problems and generate plots run

```
python run_maros.py && python analyze_maros.py
```


To run the benchmark problems, first create an empty directory called `generated_solvers/` in the root of this repository then run

```
python generate_solvers.py && python run_benchmarks.py
```
Before running the benchmark problems, the user must generate the cvxgen solvers using the problem files in the `cvxgen/problems/` directory and place them in a directory called `generated_solvers/` within the `cvxgen/` directory.

## Citing
```
@misc{chari2025qoco,
  title         = {QOCO: A Quadratic Objective Conic Optimizer with Custom Solver Generation},
  author        = {Chari, Govind M and A{\c{c}}{\i}kme{\c{s}}e, Beh{\c{c}}et},
  year          = {2025},
  eprint        = {2503.12658},
  archiveprefix = {arXiv},
  primaryclass  = {math.OC},
  url           = {https://arxiv.org/abs/2503.12658}
}
```
