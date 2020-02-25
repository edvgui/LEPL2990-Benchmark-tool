import time
import matplotlib.pyplot as plt

from src.docker import Docker
from src.inginious import Inginious
from src.podman import Podman
from src.runc import RunC


def plot(graphs, title):
    for (x, y, label) in graphs:
        plt.plot(x, y, label=label)

    plt.xlabel('Number of parallel containers')
    plt.ylabel('Time to launch (in s)')
    plt.title(title)
    plt.legend()
    plt.show()


def warm_up(tool):
    print('Warming up ' + str(tool.get_name()))
    for i in range(1, 11):
        tool.launch_many(i)


def test_number(tool, rep=1, start=1, end=10, sync=True):
    print('name, concurrent, full, time')
    x, y = [], []
    for i in range(start, end + 1):
        x.append(i)
        total = 0
        for j in range(1, rep):
            top = time.time()
            tool.launch_many(i, sync)
            total += time.time() - top
            if not sync:
                time.sleep(2)

        y.append(total / rep)
        print(str(tool.get_name()) + ', ' + str(i) + ', ' + str(sync) + ', ' + str(total / rep))

    return x, y


def test_io(tool, rep=1):
    print('name, read, write')
    read, write = 0, 0
    for i in range(1, rep):
        start = time.time()
        tool.launch_read()
        read += time.time() - start

        start = time.time()
        tool.launch_write()
        write += time.time() - start

    print(str(tool.get_name()) + ', ' + str(read / rep) + ', ' + str(write / rep))


if __name__ == "__main__":
    tools = [Docker(), Inginious(), Podman(), RunC()]

    print('Container io tests')
    for tool in tools:
        warm_up(tool)
        test_io(tool, rep=5)

    graphs = []
    print('Full execution')
    for tool in tools:
        warm_up(tool)
        x, y = test_number(tool, rep=5, start=1, end=10, sync=True)
        graphs.append((x, y, tool.get_name()))
    plot(graphs, 'Full execution')

    graphs = []
    print('Container launch only')
    for tool in tools:
        warm_up(tool)
        x, y = test_number(tool, rep=5, start=1, end=10, sync=False)
        graphs.append((x, y, tool.get_name()))
    plot(graphs, 'Container launch only')
