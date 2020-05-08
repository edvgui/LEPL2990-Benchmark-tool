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


container_managers = {
    "docker": {
        "name": "Docker",
        "default-image": "alpine",
        "images": {
            "alpine": {
                "name": "Alpine"
            },
            "centos": {
                "name": "Centos"
            }
        },
        "runtimes": {
            "runc": {
                "name": "runc",
                "path": "/usr/bin/runc"
            },
            "crun": {
                "name": "crun",
                "path": "/usr/bin/crun"
            },
            "kata-qemu": {
                "name": "kata-qemu",
                "path": "/opt/kata/bin/kata-qemu"
            },
            "kata-fc": {
                "name": "kata-fc",
                "path": "/opt/kata/bin/kata-fc"
            },
            "kata-runtime": {
                "name": "kata-runtime",
                "path": "/usr/bin/kata-runtime"
            }
        }
    },
    "podman": {
        "name": "Podman",
        "default-image": "alpine",
        "images": {
            "alpine": {
                "name": "Alpine"
            },
            "centos": {
                "name": "Centos"
            }
        },
        "runtimes": {
            "runc": {
                "name": "runc",
                "path": "/usr/bin/runc"
            },
            "crun": {
                "name": "crun",
                "path": "/usr/bin/crun"
            }
        }
    },
    "lxc": {
        "name": "LXD",
        "default-image": "alpine",
        "images": {
            "alpine": {
                "name": "Alpine"
            }
        },
        "runtimes": {}
    },
    "contingious": {
        "name": "ContINGIous",
        "default-image": "alpine",
        "images": {
            "alpine": {
                "name": "Alpine"
            }
        },
        "runtimes": {
            "runc": {
                "name": "runc",
                "path": "/usr/bin/runc"
            },
            "crun": {
                "name": "crun",
                "path": "/usr/bin/crun"
            }
        }
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


def measure(procedures, container_manager, base_image, runtime=None, warm_up=True):
    """
    Make measurement of given procedures for a specified solution
    :param runtime: The runtime to use for the tests
    :param base_image: The base image tu use for the tests
    :param container_manager: The container manager to use for the test
    :param procedures: The tests to make
    :param warm_up: Whether to warm the solution before the tests or not
    :return: The measurements made
    """
    if warm_up:
        print("\t - Warming up")
        execute(lambda: WarmUp().functions[container_manager](base_image, runtime), WarmUp().response_len(), 10)
    measurements = {}
    for procedure in procedures:
        print("\t - " + procedure.name())
        measurements[procedure.name()] = {
            "name": procedure.name(),
            "legend": procedure.response_legend(),
            "data": execute(lambda: procedure.functions[container_manager](base_image, runtime), procedure.response_len(), 10, False)
        }

    return measurements


def usage():
    usage_msg = "Usage: python3 main.py [OPTIONS] SOLUTION1 [ARGS] [SOLUTION2 [ARGS]..]\n" \
                "\n" \
                "Execute all the tests minus those specified in flags for the solutions passed in argument\n\n" \
                "Options:\n" \
                "  -h, --help               Display this message\n" \
                "  -o, --output PATH        The directory in which save the results\n" \
                "      --full               Execute all the tests\n" \
                "      --warm-up            Execute the warm up phase\n" \
                "      --hello-world        Execute hello world tests\n" \
                "      --http-server        Execute http server tests\n" \
                "      --database-read      Execute database read tests\n" \
                "      --database-write     Execute database write tests\n" \
                "      --ping               Execute network tests\n" \
                "\n" \
                "Args:\n" \
                "      --image STRING       The base image to use for the tests (overwrite the default one)\n" \
                "      --runtime STRING     The runtime to use for the tests (overwrite the default one)\n" \
                "  -t, --tag STRING         A tag to add to the output file\n" \
                "\n" \
                "Solutions:\n"

    for ctnr_mngr in container_managers.keys():
        container_manager = container_managers[ctnr_mngr]
        default_image = container_manager["default-image"]
        images = container_manager["images"]
        runtimes = container_manager["runtimes"]
        usage_msg += "  - name: %s\n" \
                     "    images: (default=%s) %s\n" \
                     "    runtimes: %s\n" \
                     "" % (ctnr_mngr, default_image, ", ".join(images.keys()), ", ".join(runtimes.keys()))
    print(usage_msg)


def main(argv):
    output = os.path.join("/".join(argv[0].split("/")[0:-1]), '../../measurements')
    warm_up = False
    hello_world = False
    http_server = False
    database_read = False
    database_write = False
    ping = False

    try:
        opts, args = getopt.getopt(argv[1:], "ho:", ["help", "output=", "full", "warm-up", "hello-world",
                                                     "http-server", "database-read", "database-write",
                                                     "ping"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-o", "--output"):
            output = arg
        elif opt == "--warm-up":
            warm_up = True
        elif opt == "--hello-world":
            hello_world = True
        elif opt == "--http-server":
            http_server = True
        elif opt == "--database-read":
            database_read = True
        elif opt == "--database-write":
            database_write = True
        elif opt == "--ping":
            ping = True
        elif opt == "--full":
            warm_up = True
            hello_world = True
            http_server = True
            database_read = True
            database_write = True
            ping = True

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

    while len(args) > 0:
        solution = args[0]
        if solution not in container_managers.keys():
            print("ERROR: this solution is not available: %s\nPick one from: %s\nuse --help for help"
                  % (solution, ", ".join(container_managers.keys())))
            sys.exit(1)

        name = container_managers[solution]["name"]
        image = container_managers[solution]["default-image"]
        runtime = None
        tag = None

        try:
            opts, args = getopt.getopt(args[1:], "t:", ["image=", "runtime=", "tag="])
        except getopt.GetoptError:
            usage()
            sys.exit(2)

        for opt, arg in opts:
            if opt == '--image':
                if arg not in container_managers[solution]["images"].keys():
                    print("ERROR: this image is not available: %s\nPick one from: %s\nuse --help for help"
                          % (arg, ", ".join(container_managers[solution]["images"].keys())))
                    sys.exit(2)
                image = arg
            elif opt == '--runtime':
                if arg not in container_managers[solution]["runtimes"].keys():
                    print("ERROR: this runtime is not available: %s\nPick one from: %s\nuse --help for help"
                          % (arg, ", ".join(container_managers[solution]["runtimes"].keys())))
                    sys.exit(2)
                runtime = arg
            elif opt in ('-t', '--tag'):
                tag = arg
            else:
                usage()
                sys.exit(2)

        print("INFO: starting measurement for %s: %s" % (name, {"image": image, "runtime": runtime, "tag": tag}))
        results = {
            "name": "%s - %s\n%s\n%s" % (name, image, runtime, tag),
            "measurements": measure(procedures, container_manager=solution, base_image=image, runtime=runtime, warm_up=warm_up)
        }
        output_file = os.path.join(output, '%s-%s-%s-%s.json' % (solution, image, runtime, tag))
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
