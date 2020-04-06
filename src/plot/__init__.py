import matplotlib.pyplot as plt
import os
import json

from plot.results_operations import results_means, plot_group


def plot_phases(measurement):
    colors = ['#4D525A', '#8F9CB3', '#3E7DCC', '#92CAD1', '#79CCB3', '#D6D727', '#E9724D']
    solutions = sorted(measurement["solutions"], key=lambda i: i["name"], reverse=True)
    solutions_m = results_means(solutions)

    plt.figure(figsize=(10, 4))
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

    # Legend
    labels = measurement["legend"]
    labels.reverse()
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(0, len(labels))]
    plt.legend(handles, labels)

    plt.grid(linestyle=':')
    plt.barh(left, height, tick_label=tick_label, color=color, align='center')
    plt.boxplot([solution["data"][-1] for solution in solutions], manage_ticks=False, showfliers=False, vert=False)
    plt.xlabel('Time (s)')
    plt.title(measurement["name"])
    plt.savefig(os.path.join(plots_folder, measurement["name"] + ".png"))


def plot_progression():
    pass


if __name__ == "__main__":
    measurements_folder = '../../measurements'
    plots_folder = '../../plots'

    solutions = {}

    files = list(filter(lambda x: os.path.isfile(os.path.join(measurements_folder, x)), os.listdir(measurements_folder)))
    for file in files:
        with open(os.path.join(measurements_folder, file), 'r') as f:
            tags = file.split('.json')
            if len(tags) == 2:
                solutions[tags[0]] = json.load(f)
            f.close()

    plot_groups = plot_group(solutions)

    def plot_if_tag(tag):
        if tag in plot_groups:
            plot_phases(plot_groups[tag])

    plot_if_tag("Hello World")
    plot_if_tag("Http server")
    plot_if_tag("Network")
    plot_if_tag("Database read xl")
    plot_if_tag("Database write xl")

    plt.show()
