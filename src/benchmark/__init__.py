from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os

from benchmark.procedure.example import Example
from benchmark.procedure.hello_world import HelloWorld
from benchmark.procedure.http_server import HttpServer
from benchmark.procedure.db_read import DatabaseRead
from benchmark.procedure.db_write import DatabaseWrite
from benchmark.procedure.network import Network
from benchmark.procedure.warm_up import WarmUp


def execute(function, response_len, repetition=5, parallelize=False):
    """
    Execute a function passed in argument the number of times repetition specifies
    :param function: The function to execute
    :param response_len: The number of element in the function return value
    :param repetition: The number of time to repeat the execution
    :param parallelize: Whether to parallelize the execution or not
    :return: An array of size response_len*repetition, which contains each return value of the execution
    """
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
        print("\t - " + procedure.name())
        results[procedure.name()] = execute(procedure.functions[solution], procedure.response_len(), 10, False)

    return results


if __name__ == "__main__":
    folder = '../../measurements'

    full = [HelloWorld(), DatabaseRead(), DatabaseWrite(), Network(), HttpServer()]

    todo = {
        "Docker Alpine": {
            "solution": "docker_alpine",
            "procedures": full
        },
        "Docker Centos": {
            "solution": "docker_centos",
            "procedures": full
        },
        "Podman Alpine": {
            "solution": "podman",
            "procedures": full
        },
        "LXC": {
            "solution": "lxc",
            "procedures": full
        },
        "runc": {
            "solution": "runc",
            "procedures": full
        },
    }

    for tag in todo:
        print("INFO: measuring " + tag)
        task = todo[tag]
        measurement = measure(task["solution"], task["procedures"])
        try:
            with open(os.path.join(folder, tag + '.json'), 'r') as f:
                prev = json.load(f)
                for r in measurement:
                    prev[r] = measurement[r]
                f.close()
        except FileNotFoundError:
            prev = measurement
        with open(os.path.join(folder, tag + '.json'), 'w+') as f:
            json.dump(prev, f)
            f.close()
