import csv
from collections import defaultdict

INPUT_CSV = "benchmark_generate_mpc.csv"
OUTPUT_TEX = "codegen_table_mpc.tex"

def latex_escape(s: str) -> str:
    return s.replace("_", r"\_")


def problem_group(name: str) -> str:
    # everything before the first underscore
    return name.split("_", 1)[0]


LATEX_HEADER = r"""
\footnotesize
\begin{longtable}{lrrrrr}
\caption{\bf Code generation time, compilation time, and resulting code and binary sizes for mpc problem instances.}
\label{tab:codegen_stats_mpc} \\

\toprule
Problem & Size & Codegen Time (s) & Compile Time (s) & Code Size (KB) & Binary Size (KB) \\
\midrule
\endfirsthead

\toprule
Problem & Size & Codegen Time (s) & Compile Time (s) & Code Size (KB) & Binary Size (KB) \\
\midrule
\endhead

\midrule
\multicolumn{6}{r}{\footnotesize Continued on next page} \\
\endfoot

\bottomrule
\endlastfoot
""".lstrip()


LATEX_FOOTER = r"""
\end{longtable}
""".lstrip()


def main():
    with open(INPUT_CSV, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # sort rows alphabetically by name
    rows.sort(key=lambda r: r["name"])

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
                f.write(
                    f"{latex_escape(r['name'])} & "
                    f"{r['size']} & "
                    f"{r['codegen_time_s']} & "
                    f"{r['compile_time_s']} & "
                    f"{r['code_size_kb']} & "
                    f"{r['binary_size_kb']} \\\\\n"
                )

        f.write(LATEX_FOOTER)


if __name__ == "__main__":
    main()
