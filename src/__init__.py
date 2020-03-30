from random import random

import matplotlib.pyplot as plt
from matplotlib import interactive

from src.results_operations import results_max, results_mean, results_medians, results_min
from src.procedure.hello_world import HelloWorld
from src.procedure.http_server import HttpServer
from src.procedure.db_read import DatabaseRead
from src.procedure.db_write import DatabaseWrite
from src.procedure.network import Network


def plot_mmm(results, title, ylabel):
    means = results_mean(results, 0.25, 0.75)

    plt.figure()
    left = [i for i in range(1, len(results) + 1)]
    tick_label = [r for r in results]
    height = [means[r] for r in results]

    plt.grid(linestyle=':')
    plt.bar(left, height, tick_label=tick_label, color=['#4D525A', '#8F9CB3', '#3E7DCC', '#92CAD1', '#79CCB3', '#D6D727', '#E9724D'], align='center')
    plt.boxplot([results[r] for r in results], manage_ticks=False, showfliers=False)
    plt.xlabel('Solutions')
    plt.ylabel(ylabel)
    plt.title(title)


test = {
    'docker_alpine': [random() for _ in range(0, 10)],
    'docker_centos': [random() for _ in range(0, 10)],
    'podman': [random() for _ in range(0, 10)],
    'lxc': [random() for _ in range(0, 10)],
    'runc': [random() for _ in range(0, 10)],
    'firecracker': [random() for _ in range(0, 10)],
    'kata': [random() for _ in range(0, 10)]
}

if __name__ == "__main__":
    interactive(True)
    plot_mmm(HelloWorld().execute(10, False), 'Hello World', 'Launching time (s)')
    plot_mmm(DatabaseRead().execute(10, False), 'Database read', 'Launching and execution time (s)')
    plot_mmm(DatabaseWrite().execute(10, False), 'Database write', 'Launching and execution time (s)')
    plot_mmm(Network().execute(10, False), 'Ping', 'Execution time (ms)')
    plot_mmm(HttpServer().execute(10, False), 'Http server', 'Launching and setup time (s)')
    interactive(False)
    plt.show()
