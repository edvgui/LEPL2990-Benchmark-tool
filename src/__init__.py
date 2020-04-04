import matplotlib.pyplot as plt
from matplotlib import interactive
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.results_operations import results_means, plot_group
from src.procedure.example import Example
from src.procedure.hello_world import HelloWorld
from src.procedure.http_server import HttpServer
from src.procedure.db_read import DatabaseRead
from src.procedure.db_write import DatabaseWrite
from src.procedure.network import Network
from src.procedure.warm_up import WarmUp


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


def execute(function, response_len, repetition=5, parallelize=False):
    results = [[] for _ in range(0, response_len)]
    if parallelize:
        with ThreadPoolExecutor(max_workers=repetition) as executor:
            threads = [executor.submit(function) for i in range(0, repetition)]
            result = list(filter(lambda i: i != -1, [future.result() for future in as_completed(threads)]))
    else:
        result = list(filter(lambda i: i != -1, [function() for i in range(0, repetition)]))

    for res in result:
        for i in range(0, response_len):
            results[i].append(res[i])

    return results


def measure(solution, procedures):
    """

    :param solution: string
    :param procedures: [ Generic() ]
    :return: { string: [ [ int ] ] }
    """
    execute(WarmUp().functions[solution], WarmUp().response_len())
    results = {}
    for procedure in procedures:
        results[procedure.name()] = execute(procedure.functions[solution], procedure.response_len(), 10, False)

    return results


if __name__ == "__main__":
    interactive(True)
    full = [HelloWorld(), DatabaseRead(), DatabaseWrite(), Network(), HttpServer()]
    measurements = {
        "Docker Alpine": measure("docker_alpine", full),
        "Docker Centos": measure("docker_centos", full),
        "Podman Alpine": measure("podman", full),
        "LXC": measure("lxc", full),
        "runc": measure("runc", full)
    }
    plot_groups = plot_group(measurements)
    for p in plot_groups:
        plot(plot_groups[p], p)
    interactive(False)
    plt.show()
