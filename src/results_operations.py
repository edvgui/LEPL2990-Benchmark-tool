import math


def check_offset_top(offset, top):
    if offset < 0:
        offset = 0
    if top > 1:
        top = 1
    if offset > top:
        offset = 0
        top = 1

    return offset, top


def results_mean(results, offset=0.0, top=1.0):
    offset, top = check_offset_top(offset, top)
    means = {}
    for r in results:
        result = results[r]
        result.sort()
        length = len(result)
        start = math.floor(offset * length)
        end = math.floor(top * length)
        tot = 0
        for m in result[start:end]:
            tot += m
        means[r] = tot / max(end - start, 1)
    return means


def results_max(results, offset=0.0, top=1.0):
    offset, top = check_offset_top(offset, top)
    maxs = {}
    for r in results:
        result = results[r]
        result.sort()
        end = math.floor(top * len(result))
        maxs[r] = result[end]
    return maxs


def results_medians(results, offset=0.0, top=1.0):
    offset, top = check_offset_top(offset, top)
    medians = {}
    for r in results:
        result = results[r]
        result.sort()
        middle = math.floor((top - offset) * len(result) / 2 + offset * len(result))
        medians[r] = result[middle]
    return medians


def results_min(results, offset=0.0, top=1.0):
    offset, top = check_offset_top(offset, top)
    mins = {}
    for r in results:
        result = results[r]
        result.sort()
        start = math.floor(offset * len(result))
        mins[r] = result[start]
    return mins