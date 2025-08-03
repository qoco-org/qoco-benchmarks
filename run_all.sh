#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Generating solvers..."
python generate_solvers.py

echo "Running benchmark problems..."
python run_benchmarks.py

echo "Running Maros benchmark..."
python run_maros.py

echo "Running SuiteSparse benchmark..."
python run_suitesparse.py

echo "Analyzing benchmark problems..."
python analyze_benchmarks.py

echo "Analyzing Maros results..."
python analyze_maros.py

echo "Analyzing SuiteSparse results..."
python analyze_suitesparse.py

echo "All tasks completed successfully."
