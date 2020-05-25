import statistics

import matplotlib.pyplot as plt
import json
import os


def plot_benchmark(solutions, image, tag):
    colors = ['#4D525A', '#8F9CB3', '#3E7DCC', '#92CAD1', '#79CCB3', '#D6D727', '#E9724D']
    plt.figure(figsize=(12, 4), dpi=150)

    sols = list(solutions.values())
    list.sort(sols, key=lambda i: i["name"])

    left, tick_label, height, color = [], [], [], []

    count = 0
    for solution in sols:
        data = solution["measurements"][image]["data"]
        list.reverse(data)
        tick_label.append("\n".join(solution["name"].split("\n")[1:]))
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
    plt.title('Runtime comparison - %s\n(Docker alpine)' % image)
    plt.savefig(os.path.join(plots_folder, "benchmark-" + "-".join(tag.split(" ")) + ".png"))


def main(plots_f, sols):
    s = [
        "docker-alpine-runc-devicemapper",
        "docker-alpine-runc-overlay",
        "docker-alpine-crun-devicemapper",
        "docker-alpine-crun-overlay",
        "docker-alpine-kata-runtime-devicemapper",
        "docker-alpine-kata-runtime-overlay",
        "docker-alpine-kata-fc-devicemapper",
    ]
    solutions = {key: value for (key, value) in sols.items() if key in s}
    plot_benchmark(solutions, "Hello World", "test")

    plt.show()


if __name__ == "__main__":
    measurements_folder = '/home/guillaume/Desktop/measurements'
    plots_folder = '../../../LEPL2990-Manuscript/images/runtime'

    __solutions = {}

    files = [f for f in os.listdir(measurements_folder) if os.path.isfile(os.path.join(measurements_folder, f))]
    for file in files:
        with open(os.path.join(measurements_folder, file), 'r') as f:
            tags = file.split('.json')
            if len(tags) == 2:
                __solutions[tags[0]] = json.load(f)
            f.close()

    main(plots_folder, __solutions)
