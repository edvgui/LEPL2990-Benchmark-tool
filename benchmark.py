import time
from docker import Docker
from inginious import Inginious
from podman import Podman
from runc import RunC


def warm_up(tool):
    print('Warming up ' + str(tool.get_name()))
    for i in range(1, 11):
        tool.launch_many(i)


def test_number(tool, rep=1, start=1, end=10, sync=True):
    for i in range(start, end + 1):
        total = 0
        for j in range(1, rep):
            top = time.time()
            tool.launch_many(i, sync)
            total += time.time() - top
            if not sync:
                time.sleep(2)

        print(str(tool.get_name()) + ', ' + str(i) + ', ' + str(sync) + ', ' + str(total / rep))


if __name__ == "__main__":
    tools = [Docker(), Inginious(), Podman(), RunC()]
    for tool in tools:
        warm_up(tool)
        test_number(tool, rep=5, start=1, end=10, sync=True)
        test_number(tool, rep=5, start=1, end=10, sync=False)
