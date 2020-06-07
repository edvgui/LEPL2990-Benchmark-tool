import copy
import statistics

import matplotlib.pyplot as plt
import json
import os
from matplotlib import rcParams


rcParams.update({'figure.autolayout': True})


def plot_benchmark(solutions, image, title, tag, label=lambda x: "\n".join(x.split("\n")[1:])):
    colors = ['#4D525A', '#8F9CB3', '#3E7DCC', '#92CAD1', '#79CCB3', '#D6D727', '#E9724D']

    sols = copy.deepcopy(list(solutions.values()))
    list.sort(sols, key=lambda i: label(i["name"]), reverse=True)

    left, tick_label, height, color = [], [], [], []

    count = 0
    for solution in sols:
        data = solution["measurements"][image]["data"]
        list.reverse(data)
        tick_label.append(label(solution["name"]))
        tick_label.extend(['' for _ in range(0, max(len(data) - 1, 0))])
        color.extend(colors[:len(data)])
        count += 1
        for d in data:
            list.sort(d)
            height.append(statistics.mean(d))

            left.append(count)

    color.reverse()

    # Legend
    labels = sols[0]["measurements"][image]["legend"]
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(0, len(labels))]
    plt.legend(handles, labels)

    plt.grid(linestyle=':')
    plt.barh(left, height, tick_label=tick_label, color=color, align='center')
    plt.boxplot([solution["measurements"][image]["data"][0] for solution in sols], manage_ticks=False, showfliers=True, vert=False)
    plt.xlabel('Time (s)')
    plt.title('%s - %s\n(%s)' % (title, image, tag))


def plot_container_creation(io_solutions, images, title, y_label='Image size (XB)', tag='Test tag', log_y=True, label=lambda x: x.split("\n")[-1]):
    list.sort(images, key=lambda i: i["size"])

    sols = list(io_solutions.keys())
    list.sort(sols)

    for s in sols:
        solution = io_solutions[s]
        x = []
        y = []
        for image in images:
            x.append(image["size"])
            measurement = solution["measurements"][image["name"]]
            data = measurement["data"][0]
            list.sort(data)
            y.append(statistics.mean(data[0:-5]))

        plt.plot(x, y, label=label(solution["name"]), marker='.')

    plt.grid(linestyle=':')
    if log_y:
        plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel(y_label)
    plt.title(title + ' - Container creation\n(' + tag + ')')
    plt.legend()


def plot_container_execution(io_solutions, images, title, y_label='Image size (XB)', tag='Test tag', log_y=True, label=lambda x: x.split("\n")[-1]):
    list.sort(images, key=lambda i: i["size"])

    sols = list(io_solutions.keys())
    list.sort(sols)

    for s in sols:
        solution = io_solutions[s]
        x = []
        y = []
        for image in images:
            x.append(image["size"])
            measurement = solution["measurements"][image["name"]]
            data = [measurement["data"][2][i] - measurement["data"][1][i] for i in range(0, len(measurement["data"][0]))]
            list.sort(data)
            y.append(statistics.mean(data[0:-5]))

        plt.plot(x, y, label=label(solution["name"]), marker='.')

    plt.grid(linestyle=':')
    if log_y:
        plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel(y_label)
    plt.title(title + ' - Container execution\n(' + tag + ')')
    plt.legend()


def main(plots_f, sols):

    # # #
    # Comparing rootless with non-rootless containers
    s = [
        "podman-alpine-crun-overlay",
        "podman-alpine-crun-overlay-rootless",
        "podman-alpine-crun-btrfs",
        "podman-alpine-crun-btrfs-rootless",
    ]
    io_solutions = {key: value for (key, value) in sols.items() if key in s}

    plt.figure(figsize=(14, 5), dpi=150)

    def label(name_array):
        labels = name_array.split("\n")
        return "-".join(labels[1:])

    tag = 'Docker Alpine - IO read'
    io_images = [
        {"name": "IO read xs", "size": 10},
        {"name": "IO read sm", "size": 100},
        {"name": "IO read md", "size": 1000},
        {"name": "IO read lg", "size": 10000},
        {"name": "IO read xl", "size": 100000}
    ]
    plt.subplot(1, 3, 1)
    plot_container_creation(io_solutions, io_images, "Rootless overhead", y_label='Number of files', tag=tag, label=label)
    plt.subplot(1, 3, 2)
    plot_container_execution(io_solutions, io_images, "Rootless overhead", y_label='Number of files', tag=tag, label=label)

    tag = 'Docker Alpine - IO write'
    io_images = [
        {"name": "IO write xs", "size": 10},
        {"name": "IO write sm", "size": 100},
        {"name": "IO write md", "size": 1000},
        {"name": "IO write lg", "size": 10000},
        {"name": "IO write xl", "size": 100000}
    ]
    plt.subplot(1, 3, 3)
    plot_container_execution(io_solutions, io_images, "Rootless overhead", y_label='Number of files', tag=tag,
                             log_y=True, label=label)

    plt.savefig(os.path.join(plots_folder, "question-3-rootless-io.png"))

    # # #
    # Comparing virtualized containers
    s = [
        "docker-alpine-crun-overlay",
        "docker-alpine-crun-devicemapper",
        "docker-alpine-kata-runtime-overlay",
        "docker-alpine-kata-runtime-devicemapper",
        "docker-alpine-kata-fc-devicemapper"
    ]
    io_solutions = {key: value for (key, value) in sols.items() if key in s}

    plt.figure(figsize=(14, 5), dpi=150)

    def label(name_array):
        labels = name_array.split("\n")
        return "-".join(labels[1:])

    tag = 'Docker Alpine - IO read'
    io_images = [
        {"name": "IO read xs", "size": 10},
        {"name": "IO read sm", "size": 100},
        {"name": "IO read md", "size": 1000},
        {"name": "IO read lg", "size": 10000},
        {"name": "IO read xl", "size": 100000}
    ]
    plt.subplot(1, 3, 1)
    plot_container_creation(io_solutions, io_images, "Virtualization impact", y_label='Number of files', tag=tag,
                            label=label)
    plt.subplot(1, 3, 2)
    plot_container_execution(io_solutions, io_images, "Vitualization impact", y_label='Number of files', tag=tag,
                             label=label)

    tag = 'Docker Alpine - IO write'
    io_images = [
        {"name": "IO write xs", "size": 10},
        {"name": "IO write sm", "size": 100},
        {"name": "IO write md", "size": 1000},
        {"name": "IO write lg", "size": 10000},
        {"name": "IO write xl", "size": 100000}
    ]
    plt.subplot(1, 3, 3)
    plot_container_execution(io_solutions, io_images, "Virtualization impact", y_label='Number of files', tag=tag,
                             log_y=True, label=label)

    plt.savefig(os.path.join(plots_folder, "question-3-virtualization-io.png"))

    plt.figure(figsize=(14, 5), dpi=150)

    def label(name_array):
        labels = name_array.split("\n")
        return "-".join(labels[1:])

    tag = 'Docker Alpine - Database write'
    io_images = [
        {"name": "Database write xs", "size": 151.552},
        {"name": "Database write sm", "size": 536.576},
        {"name": "Database write md", "size": 2646.016},
        {"name": "Database write lg", "size": 11931.648},
        {"name": "Database write xl", "size": 111558.656}
    ]
    plt.subplot(1, 3, 1)
    plot_container_creation(io_solutions, io_images, "Virtualization impact", y_label='Database size (KB)', tag=tag, label=label)
    plt.subplot(1, 3, 2)
    plot_container_execution(io_solutions, io_images, "Virtualization impact", y_label='Database size (KB)', tag=tag, label=label)

    tag = 'Docker Alpine - Database read'
    io_images = [
        {"name": "Database read xs", "size": 151.552},
        {"name": "Database read sm", "size": 536.576},
        {"name": "Database read md", "size": 2646.016},
        {"name": "Database read lg", "size": 11931.648},
        {"name": "Database read xl", "size": 111558.656}
    ]
    plt.subplot(1, 3, 3)
    plot_container_execution(io_solutions, io_images, "Virtualization impact", y_label='Database size (KB)', tag=tag,
                             log_y=True, label=label)

    plt.savefig(os.path.join(plots_folder, "question-3-virtualization-db.png"))

    # plt.show()


if __name__ == "__main__":
    measurements_folder = '/home/guillaume/Desktop/measurements'
    plots_folder = '../../../LEPL2990-Manuscript/images'

    solutions = {}

    files = [f for f in os.listdir(measurements_folder) if os.path.isfile(os.path.join(measurements_folder, f))]
    for file in files:
        with open(os.path.join(measurements_folder, file), 'r') as f:
            tags = file.split('.json')
            if len(tags) == 2:
                solutions[tags[0]] = json.load(f)
            f.close()

    main(plots_folder, solutions)
