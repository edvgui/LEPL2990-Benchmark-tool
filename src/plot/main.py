import matplotlib.pyplot as plt
import os
import json
from matplotlib import rcParams

from results_operations import benchmark_means, group_benchmarks, io_means, group_ios


rcParams.update({'figure.autolayout': True})


def plot_benchmark(measurement, tag):
    colors = ['#4D525A', '#8F9CB3', '#3E7DCC', '#92CAD1', '#79CCB3', '#D6D727', '#E9724D']
    solutions = sorted(measurement["solutions"], key=lambda i: i["name"], reverse=True)
    solutions_m = benchmark_means(solutions)

    plt.figure(figsize=(10, len(solutions) / 4 * 3 + 0.5), dpi=150)
    left, tick_label, height, color = [], [], [], []
    count = 0
    for solution_m in solutions_m:
        means = solution_m["means"]
        means.reverse()
        height.extend(means)

        tick_label.append(solution_m["name"])
        tick_label.extend(['' for _ in range(0, max(len(means) - 1, 0))])

        count += 1
        left.extend([count for _ in range(0, len(means))])

        color.extend(colors[:len(means)])

    color.reverse()

    # Legend
    labels = measurement["legend"]
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(0, len(labels))]
    plt.legend(handles, labels)

    plt.grid(linestyle=':')
    plt.barh(left, height, tick_label=tick_label, color=color, align='center')
    plt.boxplot([solution["data"][-1] for solution in solutions], manage_ticks=False, showfliers=True, vert=False)
    plt.xlabel('Time (s)')
    plt.title(measurement["name"] + ' (' + tag + ')')
    plt.savefig(os.path.join(plots_folder, "Benchmark - " + tag + " - " + measurement["name"] + ".png"))


def plot_io(plots, phase, name, tag):
    plots_m = io_means(plots, phase)

    plt.figure(figsize=(10, 4), dpi=150)
    for plot_m in plots_m:
        plt.plot(plot_m["x"], plot_m["y"], label=plot_m["name"], marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel('Database file size (MB)')
    plt.title('I/O Tests  - ' + name + ' (' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "IO Tests - " + tag + " - " + name + ".png"))


def plot_benchmarks(plots, tag):
    for p in plots:
        plot_benchmark(plots[p], tag)


def plot_ios(io_s, tag):
    io_solutions = {key: value for (key, value) in solutions.items() if key in io_s}

    # Read tests total
    plot_io(group_ios(io_solutions, ["Database read xs", "Database read sm", "Database read md", "Database read lg",
                                     "Database read xl"]), -1, 'Read execution', tag)

    # Write tests total
    plot_io(group_ios(io_solutions, ["Database write xs", "Database write sm", "Database write md",
                                     "Database write lg", "Database write xl"]), -1, 'Write execution', tag)

    # Read tests creation
    plot_io(group_ios(io_solutions, ["Database read xs", "Database read sm", "Database read md", "Database read lg",
                                     "Database read xl"]), 0, 'Read creation', tag)

    # Write tests creation
    plot_io(group_ios(io_solutions, ["Database write xs", "Database write sm", "Database write md",
                                     "Database write lg", "Database write xl"]), 0, 'Write creation', tag)


if __name__ == "__main__":
    measurements_folder = '../../measurements'
    plots_folder = '../../plots'

    solutions = {}

    files = [f for f in os.listdir(measurements_folder) if os.path.isfile(os.path.join(measurements_folder, f))]
    for file in files:
        with open(os.path.join(measurements_folder, file), 'r') as f:
            tags = file.split('.json')
            if len(tags) == 2:
                solutions[tags[0]] = json.load(f)
            f.close()

    # # #
    # Docker alpine
    tag = 'Docker alpine'
    s = ["docker-alpine-overlay2", "docker-alpine-aufs", "docker-alpine-vfs", "docker-alpine-devicemapper",
         "docker-alpine-btrfs", "docker-alpine-zfs"]
    t = ["Hello World", "Http server", "Database read xl", "Database write xl"]
    benchmark_solutions = {key: value for (key, value) in solutions.items() if key in s}
    plot_benchmarks(group_benchmarks(benchmark_solutions, t), tag)
    #plot_ios(s, tag)

    # # #
    # Docker centos
    tag = 'Docker centos'
    s = ["docker-centos-overlay2", "docker-centos-aufs", "docker-centos-vfs", "docker-centos-devicemapper",
         "docker-centos-btrfs", "docker-centos-zfs"]
    benchmark_solutions = {key: value for (key, value) in solutions.items() if key in s}
    #plot_benchmarks(group_benchmarks(benchmark_solutions, t), tag)
    #plot_ios(s, tag)

    # # #
    # Podman alpine
    tag = 'Podman alpine'
    s = ["podman-alpine-overlay", "podman-alpine-vfs"]
    benchmark_solutions = {key: value for (key, value) in solutions.items() if key in s}
    #plot_benchmarks(group_benchmarks(benchmark_solutions, t), tag)
    #plot_ios(s, tag)

    # # #
    # LXC alpine
    tag = 'LXC alpine'
    s = ["lxc-alpine-btrfs", "lxc-alpine-zfs", "lxc-alpine-dir", "lxc-alpine-lvm"]
    benchmark_solutions = {key: value for (key, value) in solutions.items() if key in s}
    #plot_benchmarks(group_benchmarks(benchmark_solutions, t), tag)
    #plot_ios(s, tag)

    # # #
    # Qemu alpine
    tag = 'Qemu alpine'
    s = ["qemu-alpine-overlay2", "qemu-alpine-aufs", "qemu-alpine-vfs", "qemu-alpine-devicemapper",
         "qemu-alpine-btrfs", "qemu-alpine-zfs"]
    benchmark_solutions = {key: value for (key, value) in solutions.items() if key in s}
    #plot_benchmarks(group_benchmarks(benchmark_solutions, t), tag)
    #plot_ios(s, tag)

    # # #
    # Firecracker alpine
    tag = 'Firecracker alpine'
    s = ["firecracker-alpine-devicemapper", "firecracker-alpine-devicemapper-loopback"]
    benchmark_solutions = {key: value for (key, value) in solutions.items() if key in s}
    #plot_benchmarks(group_benchmarks(benchmark_solutions, t), tag)
    #plot_ios(s, tag)

    # # #
    # All
    tag = 'All'
    s = ["docker-alpine-overlay2", "docker-centos-overlay2", "podman-alpine-overlay", "runc-alpine", "lxc-alpine-zfs",
         "qemu-alpine-overlay2", "firecracker-alpine-devicemapper"]
    t = ["Hello World", "Http server", "Database read xl", "Database write xl", "Network"]
    benchmark_solutions = {key: value for (key, value) in solutions.items() if key in s}
    #plot_benchmarks(group_benchmarks(benchmark_solutions, t), tag)
    #plot_ios(s, tag)

    plt.show()
