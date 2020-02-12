import time
from docker import Docker
from inginious import Inginious
from podman import Podman


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
    test_number(Docker(), rep=5, start=1, end=10, sync=True)
    test_number(Docker(), rep=5, start=1, end=10, sync=False)
    test_number(Inginious(), rep=5, start=1, end=10, sync=True)
    test_number(Inginious(), rep=5, start=1, end=10, sync=False)
    test_number(Podman(), rep=5, start=1, end=10, sync=True)
    test_number(Podman(), rep=5, start=1, end=10, sync=False)
