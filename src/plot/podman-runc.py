import matplotlib.pyplot as plt
import json
import os

import plots
import results_operations


def main(plots_f, sols):
    # # #
    # Docker alpine runc
    tag = 'Podman alpine runc'
    s = [
        "podman-alpine-runc-aufs",
        # "podman-alpine-runc-btrfs",
        "podman-alpine-runc-overlay",
        "podman-alpine-runc-vfs",
        "podman-alpine-runc-zfs"
    ]
    t = ["Hello World", "Http server", "Network", "Ping"]
    benchmark_solutions = {key: value for (key, value) in sols.items() if key in s}
    plots.plot_benchmarks(results_operations.group_benchmarks(benchmark_solutions, t), tag, plots_f)
    plots.plot_ios(sols, s, tag, plots_f)
    plots.plot_dbs(sols, s, tag, plots_f)

    # # #
    # Docker centos runc
    tag = 'Podman centos runc'
    s = [
        "podman-centos-runc-aufs",
        "podman-centos-runc-btrfs",
        "podman-centos-runc-overlay",
        # "podman-centos-runc-vfs",
        "podman-centos-runc-zfs"
    ]
    t = ["Hello World", "Http server", "Network", "Ping"]
    benchmark_solutions = {key: value for (key, value) in sols.items() if key in s}
    plots.plot_benchmarks(results_operations.group_benchmarks(benchmark_solutions, t), tag, plots_f)
    plots.plot_ios(sols, s, tag, plots_f)
    plots.plot_dbs(sols, s, tag, plots_f)

    plt.show()


if __name__ == "__main__":
    measurements_folder = '/home/guillaume/Desktop/measurements'
    plots_folder = '../../plots'

    solutions = {}

    files = [f for f in os.listdir(measurements_folder) if os.path.isfile(os.path.join(measurements_folder, f))]
    for file in files:
        with open(os.path.join(measurements_folder, file), 'r') as f:
            tags = file.split('.json')
            if len(tags) == 2:
                solutions[tags[0]] = json.load(f)
            f.close()

    main(plots_folder, solutions)
