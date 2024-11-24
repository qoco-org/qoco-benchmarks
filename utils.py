import numpy as np
import os, shutil


def get_average_solvetime(df):
    size = set(df["size"])
    size = [*size]
    size.sort()
    time = []
    for sz in size:
        idx = df[df["size"] == sz].index
        time.append(np.nanmean(df["run_time"][idx]))
    return size, time


def export_figures():
    source_dir = "./plots/"
    for file_name in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file_name)
        destination_file = os.path.join("../qoco-paper/img", file_name)

        # Check if it is a file and not a directory
        if os.path.isfile(source_file):
            shutil.copy(source_file, destination_file)
