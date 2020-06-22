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
            height.append(statistics.mean(d[:-5]))

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
            data = copy.deepcopy(measurement["data"][0])
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
    # Comparing storage driver alternatives
    plt.figure(figsize=(14, 5), dpi=150)

    s = [
        "docker-centos-runc-aufs",
        "docker-centos-runc-btrfs",
        "docker-centos-runc-devicemapper",
        "docker-centos-runc-overlay",
        "docker-centos-runc-vfs",
        "docker-centos-runc-zfs"
    ]
    io_solutions = {key: value for (key, value) in sols.items() if key in s}

    tag = 'Docker centos runc - IO read'
    io_images = [
        {"name": "IO read xs", "size": 10},
        {"name": "IO read sm", "size": 100},
        {"name": "IO read md", "size": 1000},
        {"name": "IO read lg", "size": 10000},
        {"name": "IO read xl", "size": 100000}
    ]
    plt.subplot(1, 3, 1)
    plot_container_creation(io_solutions, io_images, 'Storage driver comparison', y_label='Number of files', tag=tag)
    plt.subplot(1, 3, 2)
    plot_container_execution(io_solutions, io_images, 'Storage driver comparison', y_label='Number of files', tag=tag, log_y=True)

    tag = 'Docker centos runc - Database write'
    io_images = [
        {"name": "Database write xs", "size": 151.552},
        {"name": "Database write sm", "size": 536.576},
        {"name": "Database write md", "size": 2646.016},
        {"name": "Database write lg", "size": 11931.648},
        {"name": "Database write xl", "size": 111558.656}
    ]
    plt.subplot(1, 3, 3)
    plot_container_execution(io_solutions, io_images, 'Storage driver comparison', y_label='Database size (KB)', tag=tag, log_y=False)

    plt.savefig(os.path.join(plots_folder, "question-1-storage-driver.png"))

    # # #
    # Comparing base image alternatives
    plt.figure(figsize=(14, 5), dpi=150)

    s = [
        "docker-centos-runc-btrfs",
        "docker-centos-runc-overlay",
        "docker-alpine-runc-btrfs",
        "docker-alpine-runc-overlay",
    ]
    io_solutions = {key: value for (key, value) in sols.items() if key in s}

    def label(name_array):
        labels = name_array.split("\n")
        return " - ".join([labels[0].split(" - ")[1], labels[2]])

    tag = 'Docker centos runc - IO read'
    io_images = [
        {"name": "IO read xs", "size": 10},
        {"name": "IO read sm", "size": 100},
        {"name": "IO read md", "size": 1000},
        {"name": "IO read lg", "size": 10000},
        {"name": "IO read xl", "size": 100000}
    ]
    plt.subplot(1, 3, 1)
    plot_container_creation(io_solutions, io_images, 'Base image comparison', y_label='Number of files', tag=tag, log_y=False, label=label)
    plt.subplot(1, 3, 2)
    plot_container_execution(io_solutions, io_images, 'Base image comparison', y_label='Number of files', tag=tag, log_y=True, label=label)

    tag = 'Docker centos runc - IO write'
    io_images = [
        {"name": "IO write xs", "size": 10},
        {"name": "IO write sm", "size": 100},
        {"name": "IO write md", "size": 1000},
        {"name": "IO write lg", "size": 10000},
        {"name": "IO write xl", "size": 100000}
    ]
    plt.subplot(1, 3, 3)
    plot_container_execution(io_solutions, io_images, "Base image comparison", y_label='Number of files', tag=tag, log_y=False, label=label)

    plt.savefig(os.path.join(plots_folder, "question-1-base-image.png"))

    # # #
    # Comparing runtime alternatives
    plt.figure(figsize=(14, 5), dpi=150)
    s = [
        "docker-alpine-runc-overlay",
        "docker-alpine-runc-devicemapper",
        "docker-alpine-crun-overlay",
        "docker-alpine-crun-devicemapper",
        "docker-alpine-kata-runtime-overlay",
        "docker-alpine-kata-runtime-devicemapper",
        "docker-alpine-kata-fc-devicemapper"
    ]
    io_solutions = {key: value for (key, value) in sols.items() if key in s}

    def label(name_array):
        labels = name_array.split("\n")
        return labels[-1] + "\n" + labels[1]

    tag = 'Docker alpine'
    plot_benchmark(io_solutions, "Hello World", 'Runtime comparison', tag, label=label)

    plt.savefig(os.path.join(plots_folder, "question-1-runtime.png"))

    # # #
    # Comparing container manager alternatives
    plt.figure(figsize=(14, 5), dpi=150)
    s = [
        "podman-alpine-crun-overlay",
        # "podman-alpine-crun-overlay-rootless",
        "docker-alpine-crun-overlay",
        "podman-alpine-crun-btrfs",
        # "podman-alpine-crun-btrfs-rootless",
        "docker-alpine-crun-btrfs",
        "lxd-alpine-lxc-btrfs",
    ]
    io_solutions = {key: value for (key, value) in sols.items() if key in s}

    def label(name_array):
        labels = name_array.split("\n")
        return labels[0].split(" - ")[0] + "\n" + labels[-1]

    tag = 'Alpine crun/lxc'
    plt.subplot(1, 2, 1)
    plot_benchmark(io_solutions, "Hello World", "Container manager comparison", tag, label=label)

    def label(name_array):
        labels = name_array.split("\n")
        return labels[0].split(" - ")[0] + "-" + labels[-1]

    tag = 'Alpine crun/lxc - IO read'
    io_images = [
        {"name": "IO read xs", "size": 10},
        {"name": "IO read sm", "size": 100},
        {"name": "IO read md", "size": 1000},
        {"name": "IO read lg", "size": 10000},
        {"name": "IO read xl", "size": 100000}
    ]
    plt.subplot(1, 2, 2)
    plot_container_execution(io_solutions, io_images, "Container manager comparison", y_label='Number of files', tag=tag, label=label)

    plt.savefig(os.path.join(plots_folder, "question-1-manager.png"))

    # # #
    # Comparing current solution to best solution
    plt.figure(figsize=(14, 3.5), dpi=150)
    s = [
        "docker-alpine-crun-overlay",
        "docker-centos-runc-overlay",
        "docker-centos-kata-fc-devicemapper"
    ]
    io_solutions = {key: value for (key, value) in sols.items() if key in s}

    def label(name_array):
        labels = name_array.split("\n")
        return labels[0].split(" - ")[1] + "\n" + labels[1] + "\n" + labels[2]

    tag = 'Docker'
    plot_benchmark(io_solutions, "Hello World", "Complete comparison", tag, label=label)

    plt.savefig(os.path.join(plots_folder, "question-1-final.png"))

    plt.show()


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
