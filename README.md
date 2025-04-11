# QOCO Benchmarks

This repository was used to generated the numerical results in the paper titled [QOCO: A Quadratic Objective Conic Optimizer with Custom Solver Generation](https://arxiv.org/abs/2503.12658).

To run benchmarks, first create a python 3.12 virtual environment and install the requirements with

```
pip install -r requirements.txt
```


To run the Maros-Meszaros problems and generate plots run

```
python run_maros.py && python analyze_maros.py
```

Before running the benchmark problems, the user must generate the cvxgen solvers using the problem files in the `cvxgen/problems/` directory and place them in a directory called `generated_solvers/` within the `cvxgen/` directory.

To run the benchmark problems, create a directory titled `generated_solvers/` in the root of the repository then run

```
python generate_solvers.py && python run_benchmarks.py
```

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
