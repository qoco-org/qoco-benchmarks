#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Generating solvers..."
python generate_solvers.py

echo "Running benchmark problems..."
python run_benchmarks.py

echo "Running Maros benchmark..."
python run_maros.py

echo "Analyzing Maros results..."
python analyze_maros.py

echo "All tasks completed successfully."
