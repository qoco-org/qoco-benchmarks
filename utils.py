import numpy as np

def get_average_solvetime(df):
    size = set(df["size"])
    size = [*size]
    size.sort()
    time = []
    for sz in size:
        idx = df[df["size"] == sz].index
        time.append(1000 * np.nanmean(df["run_time"][idx]))
    return size, time
