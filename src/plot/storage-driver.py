import statistics

import matplotlib.pyplot as plt
import json
import os


def plot_container_creation(io_solutions, images, y_label='Image size (XB)', tag='Test tag'):
    plt.figure(figsize=(6, 4), dpi=150)
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

        plt.plot(x, y, label=solution["name"].split("\n")[-1], marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel(y_label)
    plt.title('Storage driver comparison - Container creation\n(' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "storage-driver-creation-" + "-".join(tag.split(" ")) + ".png"))


def plot_container_startup(io_solutions, images, y_label='Image size (XB)', tag='Test tag'):
    plt.figure(figsize=(6, 4), dpi=150)
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
            data = [measurement["data"][1][i] - measurement["data"][0][i] for i in range(0, len(measurement["data"][0]))]
            list.sort(data)
            y.append(statistics.mean(data[0:-5]))

        plt.plot(x, y, label=solution["name"].split("\n")[-1], marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel(y_label)
    plt.title('Storage driver comparison - Container startup\n(' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "storage-driver-startup-" + "-".join(tag.split(" ")) + ".png"))


def plot_container_execution(io_solutions, images, y_label='Image size (XB)', tag='Test tag'):
    plt.figure(figsize=(6, 4), dpi=150)
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

        plt.plot(x, y, label=solution["name"].split("\n")[-1], marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel(y_label)
    plt.title('Storage driver comparison - Container execution\n(' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "storage-driver-execution-" + "-".join(tag.split(" ")) + ".png"))


def plot_container_full(io_solutions, images, y_label='Image size (XB)', tag='Test tag'):
    plt.figure(figsize=(6, 4), dpi=150)
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
            data = measurement["data"][-1]
            list.sort(data)
            y.append(statistics.mean(data[0:-5]))

        plt.plot(x, y, label=solution["name"].split("\n")[-1], marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel(y_label)
    plt.title('Storage driver comparison - Container creation+startup+execution\n(' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "storage-driver-full-" + "-".join(tag.split(" ")) + ".png"))


def main(plots_f, sols):
    s = [
        "docker-alpine-runc-aufs",
        "docker-alpine-runc-btrfs",
        "docker-alpine-runc-devicemapper",
        "docker-alpine-runc-overlay",
        "docker-alpine-runc-vfs",
        "docker-alpine-runc-zfs"
    ]
    io_solutions = {key: value for (key, value) in sols.items() if key in s}

    # # #
    # Docker alpine crun
    tag = 'Docker alpine runc - IO write'
    io_images = [
        {"name": "IO write xs", "size": 51.2},
        {"name": "IO write sm", "size": 471.04},
        {"name": "IO write md", "size": 4618.24},
        {"name": "IO write lg", "size": 46090.24},
        {"name": "IO write xl", "size": 460810.24}
    ]
    plot_container_creation(io_solutions, io_images, y_label='Archive size (KB)', tag=tag)
    # plot_container_startup(io_solutions, io_images, y_label='Archive size (KB)', tag=tag)
    io_images = [
        {"name": "IO write xs", "size": 10},
        {"name": "IO write sm", "size": 100},
        {"name": "IO write md", "size": 1000},
        {"name": "IO write lg", "size": 10000},
        {"name": "IO write xl", "size": 100000}
    ]
    plot_container_execution(io_solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Number of files (n)', tag=tag)

    tag = 'Docker alpine runc - IO read'
    io_images = [
        {"name": "IO read xs", "size": 10},
        {"name": "IO read sm", "size": 100},
        {"name": "IO read md", "size": 1000},
        {"name": "IO read lg", "size": 10000},
        {"name": "IO read xl", "size": 100000}
    ]
    plot_container_creation(io_solutions, io_images, y_label='Number of files (n)', tag=tag)
    # plot_container_startup(io_solutions, io_images, y_label='Number of files', tag=tag)
    plot_container_execution(io_solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Number of files (n)', tag=tag)

    tag = 'Docker alpine runc - Database read'
    io_images = [
        {"name": "Database read xs", "size": 151.552},
        {"name": "Database read sm", "size": 536.576},
        {"name": "Database read md", "size": 2646.016},
        {"name": "Database read lg", "size": 11931.648},
        {"name": "Database read xl", "size": 111558.656}
    ]
    # plot_container_creation(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    # plot_container_startup(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_execution(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Database size (KB)', tag=tag)

    tag = 'Docker alpine runc - Database write'
    io_images = [
        {"name": "Database write xs", "size": 151.552},
        {"name": "Database write sm", "size": 536.576},
        {"name": "Database write md", "size": 2646.016},
        {"name": "Database write lg", "size": 11931.648},
        {"name": "Database write xl", "size": 111558.656}
    ]
    # plot_container_creation(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    # plot_container_startup(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_execution(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Database size (KB)', tag=tag)

    s = [
        "docker-alpine-kata-runtime-aufs",
        "docker-alpine-kata-runtime-btrfs",
        "docker-alpine-kata-runtime-devicemapper",
        "docker-alpine-kata-runtime-overlay",
        "docker-alpine-kata-runtime-vfs",
        "docker-alpine-kata-runtime-zfs",
    ]
    io_solutions = {key: value for (key, value) in sols.items() if key in s}

    tag = 'Docker alpine kata - IO write'
    io_images = [
        {"name": "IO write xs", "size": 51.2},
        {"name": "IO write sm", "size": 471.04},
        {"name": "IO write md", "size": 4618.24},
        {"name": "IO write lg", "size": 46090.24},
        {"name": "IO write xl", "size": 460810.24}
    ]
    plot_container_creation(io_solutions, io_images, y_label='Archive size (KB)', tag=tag)
    plot_container_startup(io_solutions, io_images, y_label='Archive size (KB)', tag=tag)
    io_images = [
        {"name": "IO write xs", "size": 10},
        {"name": "IO write sm", "size": 100},
        {"name": "IO write md", "size": 1000},
        {"name": "IO write lg", "size": 10000},
        {"name": "IO write xl", "size": 100000}
    ]
    plot_container_execution(io_solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Number of files (n)', tag=tag)

    tag = 'Docker alpine kata - IO read'
    io_images = [
        {"name": "IO read xs", "size": 10},
        {"name": "IO read sm", "size": 100},
        {"name": "IO read md", "size": 1000},
        {"name": "IO read lg", "size": 10000},
        {"name": "IO read xl", "size": 100000}
    ]
    plot_container_creation(io_solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_startup(io_solutions, io_images, y_label='Number of files', tag=tag)
    plot_container_execution(io_solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Number of files (n)', tag=tag)

    tag = 'Docker alpine kata - Database read'
    io_images = [
        {"name": "Database read xs", "size": 151.552},
        {"name": "Database read sm", "size": 536.576},
        {"name": "Database read md", "size": 2646.016},
        {"name": "Database read lg", "size": 11931.648},
        {"name": "Database read xl", "size": 111558.656}
    ]
    # plot_container_creation(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    # plot_container_startup(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_execution(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Database size (KB)', tag=tag)

    tag = 'Docker alpine kata - Database write'
    io_images = [
        {"name": "Database write xs", "size": 151.552},
        {"name": "Database write sm", "size": 536.576},
        {"name": "Database write md", "size": 2646.016},
        {"name": "Database write lg", "size": 11931.648},
        {"name": "Database write xl", "size": 111558.656}
    ]
    # plot_container_creation(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    # plot_container_startup(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_execution(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Database size (KB)', tag=tag)

    s = [
        "lxd-alpine-lxc-btrfs",
        "lxd-alpine-lxc-dir",
        "lxd-alpine-lxc-lvm",
        "lxd-alpine-lxc-zfs"
    ]
    io_solutions = {key: value for (key, value) in sols.items() if key in s}

    tag = 'LXD alpine LXC - IO write'
    io_images = [
        {"name": "IO write xs", "size": 51.2},
        {"name": "IO write sm", "size": 471.04},
        {"name": "IO write md", "size": 4618.24},
        {"name": "IO write lg", "size": 46090.24},
        {"name": "IO write xl", "size": 460810.24}
    ]
    plot_container_creation(io_solutions, io_images, y_label='Archive size (KB)', tag=tag)
    # plot_container_startup(io_solutions, io_images, y_label='Archive size (KB)', tag=tag)
    io_images = [
        {"name": "IO write xs", "size": 10},
        {"name": "IO write sm", "size": 100},
        {"name": "IO write md", "size": 1000},
        {"name": "IO write lg", "size": 10000},
        {"name": "IO write xl", "size": 100000}
    ]
    plot_container_execution(io_solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Number of files (n)', tag=tag)

    tag = 'LXD alpine LXC - IO read'
    io_images = [
        {"name": "IO read xs", "size": 10},
        {"name": "IO read sm", "size": 100},
        {"name": "IO read md", "size": 1000},
        {"name": "IO read lg", "size": 10000},
        {"name": "IO read xl", "size": 100000}
    ]
    plot_container_creation(io_solutions, io_images, y_label='Number of files (n)', tag=tag)
    # plot_container_startup(io_solutions, io_images, y_label='Number of files', tag=tag)
    plot_container_execution(io_solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Number of files (n)', tag=tag)

    tag = 'LXD alpine LXC - Database read'
    io_images = [
        {"name": "Database read xs", "size": 151.552},
        {"name": "Database read sm", "size": 536.576},
        {"name": "Database read md", "size": 2646.016},
        {"name": "Database read lg", "size": 11931.648},
        {"name": "Database read xl", "size": 111558.656}
    ]
    # plot_container_creation(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    # plot_container_startup(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_execution(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Database size (KB)', tag=tag)

    tag = 'LXD alpine LXC - Database write'
    io_images = [
        {"name": "Database write xs", "size": 151.552},
        {"name": "Database write sm", "size": 536.576},
        {"name": "Database write md", "size": 2646.016},
        {"name": "Database write lg", "size": 11931.648},
        {"name": "Database write xl", "size": 111558.656}
    ]
    # plot_container_creation(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    # plot_container_startup(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_execution(io_solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_full(io_solutions, io_images, y_label='Database size (KB)', tag=tag)

    # plt.show()


if __name__ == "__main__":
    measurements_folder = '/home/guillaume/Desktop/measurements'
    plots_folder = '../../../LEPL2990-Manuscript/images/storage-driver'

    solutions = {}

    files = [f for f in os.listdir(measurements_folder) if os.path.isfile(os.path.join(measurements_folder, f))]
    for file in files:
        with open(os.path.join(measurements_folder, file), 'r') as f:
            tags = file.split('.json')
            if len(tags) == 2:
                solutions[tags[0]] = json.load(f)
            f.close()

    main(plots_folder, solutions)
