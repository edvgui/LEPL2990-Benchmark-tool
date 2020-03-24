import matplotlib.pyplot as plt
from matplotlib import interactive

from src.results_operations import results_max, results_mean, results_medians, results_min
from src.procedure.hello_world import HelloWorld
from src.procedure.http_server import HttpServer
from src.procedure.mondial_read import MondialRead
from src.procedure.mondial_write import MondialWrite
from src.procedure.network import Network


def plot_mmm(results, title, ylabel):
    maxs = results_max(results, 0, 0.75)
    means = results_mean(results, 0, 0.75)
    mins = results_min(results, 0, 0.75)

    plt.figure()
    left = [i for i in range(1, len(results) * 3 + 1)]
    tick_label = []
    height = []
    for r in results:
        tick_label.extend(["", r, ""])
        height.extend([maxs[r], means[r], mins[r]])

    plt.bar(left, height, tick_label=tick_label, color=['red', 'green', 'blue'])
    plt.xlabel('Solutions')
    plt.ylabel(ylabel)
    plt.title(title)


if __name__ == "__main__":
    interactive(True)
    # plot_mmm(HelloWorld().execute(10, False), 'Hello World', 'Launching time (s)')
    # plot_mmm(MondialRead().execute(10, False), 'Mondial read', 'Launching and execution time (s)')
    # plot_mmm(MondialWrite().execute(10, False), 'Mondial write', 'Launching and execution time (s)')
    plot_mmm(Network().execute(5, False), 'Ping', 'Execution time (ms)')
    # plot_mmm(HttpServer().execute(5, False), 'Http server', 'Launching and setup time (s)')
    interactive(False)
    plt.show()
