from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from benchmark.procedure.example import Example
from benchmark.procedure.hello_world import HelloWorld
from benchmark.procedure.http_server import HttpServer
from benchmark.procedure.db_read import DatabaseRead
from benchmark.procedure.db_write import DatabaseWrite
from benchmark.procedure.network import Network
from benchmark.procedure.warm_up import WarmUp


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
    full = [HelloWorld(), DatabaseRead(), DatabaseWrite(), Network(), HttpServer()]
    # measurements = {
    #     "Docker Alpine": measure("docker_alpine", full),
    #     "Docker Centos": measure("docker_centos", full),
    #     "Podman Alpine": measure("podman", full),
    #     "LXC": measure("lxc", full),
    #     "runc": measure("runc", full)
    # }

    measurements = {
        "Docker Alpine": measure("docker_alpine", [HelloWorld(), Example()])
    }

    for m in measurements:
        measurement = measurements[m]
        with open('../../measurements/' + m + '.json', 'w+') as f:
            json.dump(measurement, f)
            f.close()
