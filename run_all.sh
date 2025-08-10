#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Running Maros benchmark..."
python run_maros.py

echo "Running SuiteSparse benchmark..."
python run_suitesparse.py

echo "Generating benchmark solvers..."
python generate_benchmark_solvers.py

echo "Running benchmark problems..."
python run_benchmarks.py

echo "Generating mpc solvers..."
python generate_mpc_solvers.py

echo "Running mpc problems..."
python run_mpc.py

echo "Analyzing Maros results..."
python analyze_maros.py

echo "Analyzing SuiteSparse results..."
python analyze_suitesparse.py

echo "Analyzing benchmark problems..."
python analyze_benchmarks.py

echo "Analyzing mpc results..."
python analyze_mpc.py

echo "All tasks completed successfully."
