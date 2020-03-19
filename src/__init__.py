import matplotlib.pyplot as plt

from src.api.api_runc import create, clean
from src.procedure.hello_world import HelloWorld
from src.procedure.http_server import HttpServer
from src.procedure.mondial_read import MondialRead
from src.procedure.mondial_write import MondialWrite
from src.procedure.network import Network


def plot(graphs, title, num):
    plt.figure(num)
    for (x, y, label) in graphs:
        plt.plot(x, y, label=label)

    plt.xlabel('Number of parallel containers')
    plt.ylabel('Time to launch (in s)')
    plt.title(title)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    procs = [HelloWorld(), HttpServer(), MondialRead(), MondialWrite(), Network()]
    for p in procs:
        results = p.execute(1, False)
        print(p.name() + ": " + str(results))
