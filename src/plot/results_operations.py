def good_mean(values):
    v = sorted(values)[:-min(3, len(values))]
    return sum(v) / max(len(v), 1)


def good_median(values):
    v = sorted(values)
    return v[int(len(v) / 2)] if len(v) % 2 == 1 else (v[int(len(v) / 2)] + v[int(len(v) / 2) + 1]) / 2


def benchmark_means(solutions):
    means = []

    for solution in solutions:
        means.append({
            "name": solution["name"],
            "means": [good_mean(l) for l in solution["data"]]
        })

    return means


def group_benchmarks(solutions, benchmarks=None):
    if benchmarks is None:
        return {}

    plots = {}
    for s in solutions:
        solution = solutions[s]
        s_name = solution["name"]
        s_measurements = solution["measurements"]
        for m in s_measurements:
            measurement = s_measurements[m]
            m_name = measurement["name"]
            if m_name in benchmarks:
                m_legend = measurement["legend"]
                m_data = measurement["data"]
                if m_name not in plots:
                    plots[m_name] = {
                        "name": m_name,
                        "legend": m_legend,
                        "solutions": [{
                            "name": s_name,
                            "data": m_data
                        }]
                    }
                else:
                    plots[m_name]["solutions"].append({
                        "name": s_name,
                        "data": m_data
                    })

    return plots


def io_means(plots, phase=-1):
    means = []
    for p in plots:
        plot = plots[p]
        means.append({
            "name": plot["name"],
            "x": plot["x"],
            "y": [good_mean(l[phase]) for l in plot["y"]]
        })

    print(means)

    return means


def group_dbs(solutions, ios=None):
    if ios is None:
        return {}

    plots = {}
    for s in solutions:
        solution = solutions[s]
        s_name = solution["name"]
        s_measurements = solution["measurements"]
        plots[s_name] = {
            "name": s_name,
            "x": [0.151552, 0.536576, 2.645016, 11.931648, 111.558656],  # TODO change with database file size
            "y": [s_measurements[io]["data"] if io in s_measurements else [[]] for io in ios]
        }

    return plots


def group_ios(solutions, ios=None):
    if ios is None:
        return {}

    plots = {}
    for s in solutions:
        solution = solutions[s]
        s_name = solution["name"]
        s_measurements = solution["measurements"]
        plots[s_name] = {
            "name": s_name,
            "x": [10, 100, 1000, 10000, 100000],
            "y": [s_measurements[io]["data"] if io in s_measurements else [[]] for io in ios]
        }

    return plots