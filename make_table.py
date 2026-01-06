import csv
from collections import defaultdict

INPUT_CSV = "benchmark_generate_results.csv"
OUTPUT_TEX = "codegen_table.tex"

HEADERS = [
    "name",
    "size",
    "codegen_time_s",
    "compile_time_s",
    "code_size_kb",
    "binary_size_kb",
]

LATEX_HEADER = r"""
\begin{table}[ht]
\centering
\footnotesize
\begin{tabular}{lrrrrr}
\toprule
Problem & Size & Codegen Time (s) & Compile Time (s) & Code Size (KB) & Binary Size (KB) \\
\midrule
""".lstrip()

LATEX_FOOTER = r"""
\bottomrule
\end{tabular}
\captionsetup{labelfont=bf}
\caption{ \bf Code generation time, compilation time, and resulting code and binary sizes for benchmark problem instances.}
\label{tab:codegen_compile_stats}
\end{table}
""".lstrip()


def latex_escape(s: str) -> str:
    return s.replace("_", r"\_")


def problem_group(name: str) -> str:
    # everything up to "_N_"
    return name.split("_N_")[0]


def main():
    with open(INPUT_CSV, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # group rows by problem family
    groups = defaultdict(list)
    for row in rows:
        groups[problem_group(row["name"])].append(row)

    with open(OUTPUT_TEX, "w") as f:
        f.write(LATEX_HEADER)

        first_group = True
        for _, group_rows in groups.items():
            if not first_group:
                f.write(r"\midrule" + "\n")
            first_group = False

            for r in group_rows:
                line = (
                    f"{latex_escape(r['name'])} & "
                    f"{r['size']} & "
                    f"{r['codegen_time_s']} & "
                    f"{r['compile_time_s']} & "
                    f"{r['code_size_kb']} & "
                    f"{r['binary_size_kb']} \\\\"
                )
                f.write(line + "\n")

        f.write(LATEX_FOOTER)


if __name__ == "__main__":
    main()
