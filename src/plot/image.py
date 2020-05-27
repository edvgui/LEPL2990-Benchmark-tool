import statistics

import matplotlib.pyplot as plt
import json
import os


def plot_benchmark(solutions, image, tag):
    colors = ['#4D525A', '#8F9CB3', '#3E7DCC', '#92CAD1', '#79CCB3', '#D6D727', '#E9724D']
    plt.figure(figsize=(12, 4), dpi=150)

    sols = list(solutions.values())
    list.sort(sols, key=lambda i: i["name"], reverse=True)

    left, tick_label, height, color = [], [], [], []

    count = 0
    for solution in sols:
        data = solution["measurements"][image]["data"]
        list.reverse(data)

        labels = solution["name"].split("\n")
        label = "\n".join([labels[0].split(" - ")[1], labels[2]])
        tick_label.append(label)
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
    plt.title('Base image comparison - %s\n(Docker alpine)' % image)
    plt.savefig(os.path.join(plots_folder, "image-%s-%s.png" % ("-".join(image.split(" ")), "-".join(tag.split(" ")))))


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

        labels = solution["name"].split("\n")
        label = " - ".join([labels[0].split(" - ")[1], labels[2]])
        plt.plot(x, y, label=label, marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel(y_label)
    plt.title('Base image comparison - Container creation\n(' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "image-creation-" + "-".join(tag.split(" ")) + ".png"))


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

        labels = solution["name"].split("\n")
        label = " - ".join([labels[0].split(" - ")[1], labels[2]])
        plt.plot(x, y, label=label, marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel(y_label)
    plt.title('Base image comparison - Container startup\n(' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "image-startup-" + "-".join(tag.split(" ")) + ".png"))


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

        labels = solution["name"].split("\n")
        label = " - ".join([labels[0].split(" - ")[1], labels[2]])
        plt.plot(x, y, label=label, marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel(y_label)
    plt.title('Base image comparison - Container execution\n(' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "image-execution-%s.png" % "-".join(tag.split(" "))))


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

        labels = solution["name"].split("\n")
        label = " - ".join([labels[0].split(" - ")[1], labels[2]])
        plt.plot(x, y, label=label, marker='.')

    plt.grid(linestyle=':')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel(y_label)
    plt.title('Base image comparison - Container creation+startup+execution\n(' + tag + ')')
    plt.legend()
    plt.savefig(os.path.join(plots_folder, "image-full-" + "-".join(tag.split(" ")) + ".png"))


def main(plots_f, sols):
    tag = "Docker crun"
    s = [
        "docker-centos-crun-overlay",
        "docker-alpine-crun-overlay",
        "docker-centos-crun-btrfs",
        "docker-alpine-crun-btrfs",
    ]
    solutions = {key: value for (key, value) in sols.items() if key in s}
    # plot_benchmark(solutions, "Hello World", tag)
    # plot_benchmark(solutions, "Http server", tag)

    tag = 'Docker crun - IO read'
    io_images = [
        {"name": "IO read xs", "size": 10},
        {"name": "IO read sm", "size": 100},
        {"name": "IO read md", "size": 1000},
        {"name": "IO read lg", "size": 10000},
        {"name": "IO read xl", "size": 100000}
    ]
    plot_container_creation(solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_startup(solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_execution(solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_full(solutions, io_images, y_label='Number of files (n)', tag=tag)

    tag = 'Docker crun - IO write'
    io_images = [
        {"name": "IO write xs", "size": 51.2},
        {"name": "IO write sm", "size": 471.04},
        {"name": "IO write md", "size": 4618.24},
        {"name": "IO write lg", "size": 46090.24},
        {"name": "IO write xl", "size": 460810.24}
    ]
    plot_container_creation(solutions, io_images, y_label='Archive size (KB)', tag=tag)
    plot_container_startup(solutions, io_images, y_label='Archive size (KB)', tag=tag)
    io_images = [
        {"name": "IO write xs", "size": 10},
        {"name": "IO write sm", "size": 100},
        {"name": "IO write md", "size": 1000},
        {"name": "IO write lg", "size": 10000},
        {"name": "IO write xl", "size": 100000}
    ]
    plot_container_execution(solutions, io_images, y_label='Number of files (n)', tag=tag)
    plot_container_full(solutions, io_images, y_label='Number of files (n)', tag=tag)

    tag = 'Docker crun - Database read'
    io_images = [
        {"name": "Database read xs", "size": 151.552},
        {"name": "Database read sm", "size": 536.576},
        {"name": "Database read md", "size": 2646.016},
        {"name": "Database read lg", "size": 11931.648},
        {"name": "Database read xl", "size": 111558.656}
    ]
    plot_container_execution(solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_full(solutions, io_images, y_label='Database size (KB)', tag=tag)

    tag = 'Docker crun - Database write'
    io_images = [
        {"name": "Database write xs", "size": 151.552},
        {"name": "Database write sm", "size": 536.576},
        {"name": "Database write md", "size": 2646.016},
        {"name": "Database write lg", "size": 11931.648},
        {"name": "Database write xl", "size": 111558.656}
    ]
    plot_container_execution(solutions, io_images, y_label='Database size (KB)', tag=tag)
    plot_container_full(solutions, io_images, y_label='Database size (KB)', tag=tag)

    plt.show()


if __name__ == "__main__":
    measurements_folder = '/home/guillaume/Desktop/measurements'
    plots_folder = '../../../LEPL2990-Manuscript/images/image'

    __solutions = {}

    files = [f for f in os.listdir(measurements_folder) if os.path.isfile(os.path.join(measurements_folder, f))]
    for file in files:
        with open(os.path.join(measurements_folder, file), 'r') as f:
            tags = file.split('.json')
            if len(tags) == 2:
                __solutions[tags[0]] = json.load(f)
            f.close()

    main(plots_folder, __solutions)
