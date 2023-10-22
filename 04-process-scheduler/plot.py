#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np


def plot_progress(log_file: str, num_series: int) -> None:
    data = np.genfromtxt(log_file)

    for index in range(num_series):
        series = np.array([dat for dat in data if dat[0] == index])
        plt.plot(series[:,1], series[:,2],
                 label=f"Process{index}",
                 linestyle="None", marker="o", markersize=2.0)

    plt.xlim(0)
    plt.xlabel("Elapsed time[ms]")

    plt.ylim(0, 100)
    plt.ylabel("Progress[%]")

    plt.legend()

    plt.savefig(log_file.replace(".txt", ".png"))

    plt.close()


def plot_working_process(log_file: str, num_series: int) -> None:
    data = np.genfromtxt(log_file)

    for index in range(num_series):
        series = np.array([dat for dat in data if dat[0] == index])
        plt.plot(series[:,1], series[:,0],
                 linestyle="None", marker="o", markersize=2.0)

    plt.xlim(0)
    plt.xlabel("Elapsed time[ms]")

    plt.yticks(np.arange(0, num_series, step=1))
    plt.ylabel("Process index")

    plt.savefig(log_file.replace(".txt", "_process.png"))

    plt.close()


def plot(log_file: str, num_series: int) -> None:
    plot_progress(log_file, num_series)
    plot_working_process(log_file, num_series)


def main() -> None:
    plot("./log/1core-1process.txt", 1)
    plot("./log/1core-2process.txt", 2)
    plot("./log/1core-4process.txt", 4)

    plot("./log/2core-1process.txt", 1)
    plot("./log/2core-2process.txt", 2)
    plot("./log/2core-4process.txt", 4)

    plot("./log/1core-2process_nice.txt", 2)


if __name__ == "__main__":
    main()
