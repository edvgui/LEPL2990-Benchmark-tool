import matplotlib.pyplot as plt
import os
import json

from results_operations import benchmark_means, group_benchmarks, io_means, group_ios


def plot_benchmark(measurement):
    colors = ['#4D525A', '#8F9CB3', '#3E7DCC', '#92CAD1', '#79CCB3', '#D6D727', '#E9724D']
    solutions = sorted(measurement["solutions"], key=lambda i: i["name"], reverse=True)
    solutions_m = benchmark_means(solutions)

    plt.figure(figsize=(10, len(solutions) / 2))
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
    plt.boxplot([solution["data"][-1] for solution in solutions], manage_ticks=False, showfliers=False, vert=False)
    plt.xlabel('Time (s)')
    plt.title(measurement["name"])
    plt.savefig(os.path.join(plots_folder, "Benchmark - " + measurement["name"] + ".png"))


def plot_io(plots, phase, name):
    plots_m = io_means(plots, phase)

    plt.figure(figsize=(10, 4))
    for plot_m in plots_m:
        plt.plot(plot_m["x"], plot_m["y"], label=plot_m["name"], marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel('Database file size (MB)')
    plt.title('I/O Tests  - ' + name)
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "IO Tests - " + name + ".png"))


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

    def plot_benchmarks(plots):
        for p in plots:
            plot_benchmark(plots[p])

    # Benchmarks containers
    benchmark_s = ["docker-alpine", "docker-centos", "podman-alpine", "lxc-alpine", "runc-alpine"]
    benchmark_solutions = {key: value for (key, value) in solutions.items() if key in benchmark_s}
    plot_benchmarks(group_benchmarks(benchmark_solutions, ["Hello World", "Http server", "Database read xl",
                                                           "Database write xl", "Network"]))

    # I/O tests containers
    io_s = ["docker-alpine", "docker-centos", "podman-alpine", "lxc-alpine", "runc-alpine",
            "kata-alpine-devicemapper", "firecracker-alpine-devicemapper"]
    io_solutions = {key: value for (key, value) in solutions.items() if key in io_s}

    # Read tests total
    plot_io(group_ios(io_solutions, ["Database read xs", "Database read sm", "Database read md", "Database read lg",
                                     "Database read xl"]), -1, 'Read execution')

    # Write tests total
    plot_io(group_ios(io_solutions, ["Database write xs", "Database write sm", "Database write md", "Database write lg",
                                     "Database write xl"]), -1, 'Write execution')

    # Read tests creation
    plot_io(group_ios(io_solutions, ["Database read xs", "Database read sm", "Database read md", "Database read lg",
                                     "Database read xl"]), 0, 'Read creation')

    # Write tests creation
    plot_io(group_ios(io_solutions, ["Database write xs", "Database write sm", "Database write md", "Database write lg",
                                     "Database write xl"]), 0, 'Write creation')

    # Benchmarks vms
    benchmark_s = ["kata-alpine-devicemapper", "firecracker-alpine-devicemapper"]
    benchmark_solutions = {key: value for (key, value) in solutions.items() if key in benchmark_s}
    plot_benchmarks(group_benchmarks(benchmark_solutions, ["Hello World", "Http server", "Database read xl",
                                                           "Database write xl", "Network"]))

    # I/O tests containers
    io_s = ["kata-alpine-devicemapper", "firecracker-alpine-devicemapper"]
    io_solutions = {key: value for (key, value) in solutions.items() if key in io_s}

    # Read tests total
    plot_io(group_ios(io_solutions, ["Database read xs", "Database read sm", "Database read md", "Database read lg",
                                     "Database read xl"]), -1, 'Read execution')

    # Write tests total
    plot_io(group_ios(io_solutions, ["Database write xs", "Database write sm", "Database write md", "Database write lg",
                                     "Database write xl"]), -1, 'Write execution')

    # Read tests creation
    plot_io(group_ios(io_solutions, ["Database read xs", "Database read sm", "Database read md", "Database read lg",
                                     "Database read xl"]), 0, 'Read creation')

    # Write tests creation
    plot_io(group_ios(io_solutions, ["Database write xs", "Database write sm", "Database write md", "Database write lg",
                                     "Database write xl"]), 0, 'Write creation')


    plt.show()
