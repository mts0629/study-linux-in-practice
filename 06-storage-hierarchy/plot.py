#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np


def plot(log_file: str) -> None:
    data = np.genfromtxt(log_file)

    mem_x = [i for i in range(2, 16)]

    plt.plot(mem_x, data, linestyle="None", marker="o", markersize=3.0)

    plt.xlabel("Memory size 2^x[KiB]")
    plt.ylabel("Access time[ns/count]")
    plt.savefig(log_file.replace(".txt", ".png"))

    plt.close()


def main() -> None:
    plot("./log/cache_access.txt")


if __name__ == "__main__":
    main()
