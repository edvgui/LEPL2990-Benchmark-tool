import getopt
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os

from procedure.hello_world import HelloWorld
from procedure.http_server import HttpServer
from procedure.db_read import DatabaseRead
from procedure.db_write import DatabaseWrite
from procedure.ping import Ping
from procedure.warm_up import WarmUp


solutions = {
    "docker-alpine": {
        "name": "Docker Alpine",
        "solution": "docker_alpine",
    },
    "docker-centos": {
        "name": "Docker Centos",
        "solution": "docker_centos",
    },
    "podman-alpine": {
        "name": "Podman Alpine",
        "solution": "podman",
    },
    "lxc-alpine": {
        "name": "LXC Alpine",
        "solution": "lxc",
    },
    "runc-alpine": {
        "name": "runc Alpine",
        "solution": "runc",
    },
    "qemu-alpine": {
        "name": "Qemu Alpine",
        "solution": "qemu"
    },
    "firecracker-alpine": {
        "name": "Firecracker Alpine",
        "solution": "firecracker"
    }
}


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


def measure(solution, procedures, warm_up=True):
    """
    Make measurement of given procedures for a specified solution
    :param solution: The solution to test
    :param procedures: The tests to make
    :param warm_up: Whether to warm the solution before the tests or not
    :return: The measurements made
    """
    if warm_up:
        print("\t - Warming up")
        execute(WarmUp().functions[solution], WarmUp().response_len(), 10)
    measurements = {}
    for procedure in procedures:
        print("\t - " + procedure.name())
        measurements[procedure.name()] = {
            "name": procedure.name(),
            "legend": procedure.response_legend(),
            "data": execute(procedure.functions[solution], procedure.response_len(), 10, False)
        }

    return measurements


def usage():
    usage_msg = "Usage: python3 main.py [OPTIONS] SOLUTION1 [SOLUTION2 ...]\n" \
          "\n" \
          "Execute all the tests minus those specified in flags for the solutions passed in argument\n\n" \
          "Options:\n" \
          "  -h, --help               Display this message\n" \
          "  -o, --output string      The directory in which save the results\n" \
          "      --no-warm-up         Skip he warm up phase\n" \
          "      --no-hello-world     Skip hello world tests\n" \
          "      --no-http-server     Skip http server tests\n" \
          "      --no-database-read   Skip database read tests\n" \
          "      --no-database-write  Skip database write tests\n" \
          "      --no-ping            Skip network tests\n" \
          "\n" \
          "Solutions:\n  "
    usage_msg += "\n  ".join(solutions.keys())
    usage_msg += "\n"
    print(usage_msg)


def main(argv):
    output = os.path.join("/".join(argv[0].split("/")[0:-1]), '../../measurements')
    warm_up = True
    hello_world = True
    http_server = True
    database_read = True
    database_write = True
    ping = True

    try:
        opts, args = getopt.getopt(argv[1:], "ho:", ["help", "output=", "no-warm-up", "no-hello-world",
                                                     "no-http-server", "no-database-read", "no-database-write",
                                                     "no-ping"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-o", "--output"):
            output = arg
        elif opt == "--no-warm-up":
            warm_up = False
        elif opt == "--no-hello-world":
            hello_world = False
        elif opt == "--no-http-server":
            http_server = False
        elif opt == "--no-database-read":
            database_read = False
        elif opt == "--no-database-write":
            database_write = False
        elif opt == "--no-ping":
            ping = False

    procedures = []
    if hello_world:
        procedures.append(HelloWorld())
    if http_server:
        procedures.append(HttpServer())
    if database_read:
        procedures.extend([DatabaseRead(x) for x in ['xs', 'sm', 'md', 'lg', 'xl']])
    if database_write:
        procedures.extend([DatabaseWrite(x) for x in ['xs', 'sm', 'md', 'lg', 'xl']])
    if ping:
        procedures.append(Ping())

    if len(args) == 0:
        usage()
        sys.exit(2)

    for s in args:
        if s not in solutions.keys():
            print("ERROR: this solution is not available: " + s + "\n\tPick one from: " + ", ".join(solutions.keys()))
        else:
            solution = solutions[s]
            print("INFO: measuring " + solution["name"])
            results = {
                "name": solution["name"],
                "measurements": measure(solution["solution"], procedures, warm_up=warm_up)
            }
            output_file = os.path.join(output, s + '.json')
            try:
                with open(output_file, 'r') as f:
                    prev = json.load(f)
                    for r in results["measurements"]:
                        prev["measurements"][r] = results["measurements"][r]
                    f.close()
            except FileNotFoundError:
                prev = results
            try:
                with open(output_file, 'w+') as f:
                    json.dump(prev, f)
                    f.close()
                    print("INFO: Results written to " + output_file)
            except FileNotFoundError as e:
                print(e)
                print(prev)


if __name__ == "__main__":
    main(sys.argv)
