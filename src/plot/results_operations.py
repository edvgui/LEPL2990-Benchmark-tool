def results_means(solutions):
    means = []
    for solution in solutions:
        means.append({
            "name": solution["name"],
            "means": [sum(l)/max(len(l), 1) for l in solution["data"]]
        })

    return means


def plot_group(solutions):
    plots = {}
    for s in solutions:
        solution = solutions[s]
        s_name = solution["name"]
        s_measurements = solution["measurements"]
        for m in s_measurements:
            measurement = s_measurements[m]
            m_name = measurement["name"]
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
