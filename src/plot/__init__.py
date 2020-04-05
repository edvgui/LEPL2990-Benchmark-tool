import matplotlib.pyplot as plt
from matplotlib import interactive
import os
import json

from plot.results_operations import results_means, plot_group


def plot(results, title):
    """

    :param results: { string: [ [ int ] ] }
    :param title: string
    :return: void
    """
    colors = ['#4D525A', '#8F9CB3', '#3E7DCC', '#92CAD1', '#79CCB3', '#D6D727', '#E9724D']
    results_m = results_means(results)

    plt.figure()
    left, tick_label, height, color = [], [], [], []
    count = 0
    for r in results_m:
        means = results_m[r]
        means.reverse()
        height.extend(means)

        tick_label.append(r)
        tick_label.extend(['' for _ in range(0, max(len(means) - 1, 0))])

        count += 1
        left.extend([count for _ in range(0, len(means))])

        color.extend(colors[:len(means)])

    plt.grid(linestyle=':')
    plt.bar(left, height, tick_label=tick_label, color=color, align='center')
    plt.boxplot([results[r][-1] for r in results], manage_ticks=False, showfliers=False)
    plt.xlabel('Solutions')
    plt.ylabel('Time (s)')
    plt.title(title)


if __name__ == "__main__":
    folder = '../../measurements'

    interactive(True)
    measurements = {}

    files = list(filter(lambda x: os.path.isfile(os.path.join(folder, x)), os.listdir(folder)))
    for file in files:
        with open(os.path.join(folder, file), 'r') as f:
            tags = file.split('.json')
            if len(tags) == 2:
                measurements[tags[0]] = json.load(f)
            f.close()

    plot_groups = plot_group(measurements)
    for p in plot_groups:
        plot(plot_groups[p], p)
    interactive(False)
    plt.show()
