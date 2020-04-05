def results_means(results):
    means = {}
    for r in results:
        result = results[r]
        means[r] = [sum(l)/max(len(l), 1) for l in result]

    return means


def plot_group(measurements):
    plots = {}
    for m in measurements:
        measurement = measurements[m]
        for procedure in measurement:
            result = measurement[procedure]
            if procedure in plots:
                plots[procedure][m] = result
            else:
                plots[procedure] = {m: result}

    return plots
