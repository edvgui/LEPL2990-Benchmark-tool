import matplotlib.pyplot as plt
import os
import json
from matplotlib import rcParams

from results_operations import benchmark_means, group_benchmarks, io_means, group_ios, group_dbs


rcParams.update({'figure.autolayout': True})


def plot_benchmarks(plots, tag, plots_folder):
    for p in plots:
        __plot_benchmark(plots[p], tag, plots_folder)


def __plot_benchmark(measurement, tag, plots_folder):
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


def plot_dbs(solutions, io_s, tag, plots_folder):
    io_solutions = {key: value for (key, value) in solutions.items() if key in io_s}

    # Read tests total
    __plot_db(group_dbs(io_solutions, ["Database read xs", "Database read sm", "Database read md", "Database read lg",
                                       "Database read xl"]), -1, 'Read execution', tag, plots_folder)

    # Write tests total
    __plot_db(group_dbs(io_solutions, ["Database write xs", "Database write sm", "Database write md",
                                       "Database write lg", "Database write xl"]), -1, 'Write execution', tag, plots_folder)

    # Read tests creation
    __plot_db(group_dbs(io_solutions, ["Database read xs", "Database read sm", "Database read md", "Database read lg",
                                       "Database read xl"]), 1, 'Read start up', tag, plots_folder)

    # Write tests creation
    __plot_db(group_dbs(io_solutions, ["Database write xs", "Database write sm", "Database write md",
                                       "Database write lg", "Database write xl"]), 1, 'Write start up', tag, plots_folder)

    # Read tests creation
    __plot_db(group_dbs(io_solutions, ["Database read xs", "Database read sm", "Database read md", "Database read lg",
                                       "Database read xl"]), 0, 'Read creation', tag, plots_folder)

    # Write tests creation
    __plot_db(group_dbs(io_solutions, ["Database write xs", "Database write sm", "Database write md",
                                       "Database write lg", "Database write xl"]), 0, 'Write creation', tag, plots_folder)


def __plot_db(plots, phase, name, tag, plots_folder):
    plots_m = io_means(plots, phase)

    plt.figure(figsize=(10, 5), dpi=150)
    for plot_m in plots_m:
        plt.plot(plot_m["x"], plot_m["y"], label=plot_m["name"], marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel('Database file size (MB)')
    plt.title('Database Tests  - ' + name + ' (' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "Database Tests - " + tag + " - " + name + ".png"))


def plot_ios(solutions, io_s, tag, plots_folder):
    io_solutions = {key: value for (key, value) in solutions.items() if key in io_s}

    # Read tests total
    __plot_io(group_ios(io_solutions, ["IO read xs", "IO read sm", "IO read md", "IO read lg", "IO read xl"]), -1,
              'Read execution', tag, plots_folder)

    # Write tests total
    __plot_io(group_ios(io_solutions, ["IO write xs", "IO write sm", "IO write md", "IO write lg", "IO write xl"]), -1,
              'Write execution', tag, plots_folder)

    # Read tests creation
    __plot_io(group_ios(io_solutions, ["IO read xs", "IO read sm", "IO read md", "IO read lg", "IO read xl"]), 1,
              'Read start up', tag, plots_folder)

    # Write tests creation
    __plot_io(group_ios(io_solutions, ["IO write xs", "IO write sm", "IO write md", "IO write lg", "IO write xl"]), 1,
              'Write start up', tag, plots_folder)

    # Read tests creation
    __plot_io(group_ios(io_solutions, ["IO read xs", "IO read sm", "IO read md", "IO read lg", "IO read xl"]), 0,
              'Read creation', tag, plots_folder)

    # Write tests creation
    __plot_io(group_ios(io_solutions, ["IO write xs", "IO write sm", "IO write md", "IO write lg", "IO write xl"]), 0,
              'Write creation', tag, plots_folder)


def __plot_io(plots, phase, name, tag, plots_folder):
    plots_m = io_means(plots, phase)

    plt.figure(figsize=(10, 5), dpi=150)
    for plot_m in plots_m:
        plt.plot(plot_m["x"], plot_m["y"], label=plot_m["name"], marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of files')
    plt.title('I/O Tests  - ' + name + ' (' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "IO Tests - " + tag + " - " + name + ".png"))


def main(plots_f, sols):
    # # #
    # Docker centos/alpine runc/crun
    tag = 'Docker alpine-centos crun-runc'
    s = ["docker-centos-crun-aufs", "docker-centos-crun-overlay", "docker-centos-runc-aufs",
         "docker-centos-runc-overlay", "docker-alpine-crun-aufs", "docker-alpine-crun-overlay",
         "docker-alpine-runc-aufs", "docker-alpine-runc-overlay"]
    t = ["Hello World", "Http server", "Network", "Ping"]
    benchmark_solutions = {key: value for (key, value) in sols.items() if key in s}
    plot_benchmarks(group_benchmarks(benchmark_solutions, t), tag, plots_f)
    plot_ios(sols, s, tag, plots_f)
    plot_dbs(sols, s, tag, plots_f)

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
