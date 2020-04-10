def benchmark_means(solutions):
    means = []
    for solution in solutions:
        means.append({
            "name": solution["name"],
            "means": [sum(l)/max(len(l), 1) for l in solution["data"]]
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
            "y": [sum(l[phase]) / max(len(l[phase]), 1) for l in plot["y"]]
        })

    return means


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
            "x": [0.151552, 0.536576, 2.645016, 11.931648, 111.558656],  # TODO change with database file size
            "y": [s_measurements[io]["data"] if io in s_measurements else [[]] for io in ios]
        }

    return plots