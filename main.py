import gc
import json
import math
import random
import sys
import time

from linkedlist import LinkedList
from timer import Timer
from xfasttrie import XFastTrie
from yfasttrie import YFastTrie

def generate_random_number(n):
    return int(math.floor((random.random() * n) % n))


def generate_synthetic_data(gaps, iterations, u):
    print "Generating synthetic data for gaps: {0}".format(gaps)

    results = {}
    for g in gaps:
        print "Generating synthetic data for gap: {0}".format(g)
        data = []
        for i in xrange(iterations):
            j = 0
            dense = []
            while j < u:
                random_threshold = 4
                j += 1 + generate_random_number(random_threshold)
                dense.append(min(j, u))
            j = 0
            sparse = []
            while j < u:
                random_threshold = g / 10
                j += g - random_threshold + generate_random_number(2 * random_threshold)
                sparse.append(min(j, u))
            data.append((dense, sparse))
        results[g] = data
    return results


# performs a linear intersection between the two sets
# O(n + m) time
def intersect_linear(dense, sparse, u, build_timer, timer):
    timer.start()
    intersects = []
    x = 0
    y = 0
    while x < len(dense) and y < len(sparse):
        dx = dense[x]
        sx = sparse[y]
        if dx == sx:
            intersects.append(dx)
            x += 1
            y += 1
        elif dx < sx:
            x += 1
        else:
            y += 1
    timer.end()
    return intersects


# performs a binary search intersection between the two sets
def intersect_binary(dense, sparse, u, build_timer, timer):
    timer.start()
    intersects = []
    for i in xrange(len(sparse)):
        x = sparse[i]
        l = 0
        r = len(dense)
        while r > l:
            e = l + int(math.floor((r - l) / 2))
            y = dense[e]
            if x == y:
                intersects.append(x)
                break
            elif x < y:
                r = e
            else:
                l = e + 1
    timer.end()
    return intersects


# performs an improved binary search intersection between the two sets
def intersect_binary_improved(dense, sparse, u, build_timer, timer):
    timer.start()
    intersects = []
    l_saved = 0
    for i in xrange(len(sparse)):
        x = sparse[i]
        l = l_saved
        r = len(dense)
        while r > l:
            e = l + int(math.floor((r - l) / 2))
            y = dense[e]
            if x == y:
                intersects.append(x)
                l_saved = e
                break
            elif x < y:
                r = e
            else:
                l = e + 1
    timer.end()
    return intersects


# builds a hashtable and uses that to intersect
def intersect_hashtable(dense, sparse, u, build_timer, timer):
    build_timer.start()
    hashtable = {}
    for i in xrange(len(dense)):
        hashtable[dense[i]] = True
    build_timer.end()

    timer.start()
    intersects = []
    for i in xrange(len(sparse)):
        x = sparse[i]
        if hashtable.get(x) == True:
            intersects.append(x)
    timer.end() 
    return intersects


# builds an x-fast trie and uses that to intserect
def intersect_x_fast_trie(dense, sparse, u, build_timer, timer):
    build_timer.start()
    S = XFastTrie(dense, u)
    T = XFastTrie(sparse, u)
    build_timer.end()

    timer.start()
    intersects = []
    x = dense[0]
    y = sparse[0]
    while x is not None and y is not None:
        if x == y:
            intersects.append(x)
            x = S.successor(x)
            y = T.successor(y)
        elif x > y:
            if T.find(x):
                intersects.append(x)
            y = T.successor(x)
        else:
            if S.find(y):
                intersects.append(y)
            x = S.successor(y)
    timer.end()
    return intersects


# builds a y-fast trie and uses that to intersect
def intersect_y_fast_trie(dense, sparse, u, build_timer, timer):
    build_timer.start()
    S = YFastTrie(dense, u)
    T = YFastTrie(sparse, u)
    build_timer.end()

    timer.start()
    intersects = []
    x = dense[0]
    y = sparse[0]
    while x is not None and y is not None:
        if x == y:
            intersects.append(x)
            x = S.successor(x)
            y = T.successor(y)
        elif x > y:
            if T.find(x):
                intersects.append(x)
            y = T.successor(x)
        else:
            if S.find(y):
                intersects.append(y)
            x = S.successor(y)
    timer.end()
    return intersects


if __name__ == '__main__':
    print "==========================="
    print "|    COMP 4420 Project    |"
    print "| Aaron Wojnowski 7742591 |"
    print "==========================="
    print ""

    functions = []
    functions.append(intersect_linear)
    functions.append(intersect_binary)
    functions.append(intersect_binary_improved)
    functions.append(intersect_hashtable)
    functions.append(intersect_x_fast_trie)
    functions.append(intersect_y_fast_trie)
    function_identifiers = {
        intersect_linear : "Linear intersection",
        intersect_binary : "Binary search intersection",
        intersect_binary_improved : "Binary search intersection (improved)",
        intersect_hashtable : "Hashtable intersection",
        intersect_x_fast_trie : "X-fast trie intersection",
        intersect_y_fast_trie : "Y-fast trie intersection"
    }

    #iterations = 1000
    iterations = 1
    #gaps = [10, 100, 1000, 2000, 3000, 4000, 5000, 10000, 20000, 30000, 40000, 50000, 100000, 500000, 10000000]
    #gaps = [10, 100, 1000, 10000, 100000]
    gaps = [100, 1000, 10000, 100000]
    #u = 10000000
    u = 10000000

    print "Running test with universe {0}.".format(u)
    print "Running test with {0} iterations.".format(iterations)
    print "Running test with gaps: {0}".format(gaps)
    print ""

    synthetic_data = generate_synthetic_data(gaps, iterations, u)
    print ""

    gap_results = {}
    for g in gaps:
        print "Testing gap {0} over {1} iterations:".format(g, iterations)
        data = synthetic_data[g]
        results = {}
        for i in xrange(iterations):
            d = data[i]
            dense = d[0]
            sparse = d[1]
            verify_intersects = None
            for f in functions:
                build_timer = Timer()
                timer = Timer()
                result = f(dense, sparse, u, build_timer, timer)
                if verify_intersects is None:
                    verify_intersects = len(result)
                if len(result) != verify_intersects:
                    print "WARNING: performed {0} and received {1} intersects instead of {2}".format(f, len(result), verify_intersects)
                    sys.exit(1)
                if results.get(f) is None:
                    results[f] = []
                results[f].append((build_timer.elapsed_time, timer.elapsed_time))
            gc.collect()
        gap_result = {}
        for f in results.keys():
            build_time_sum = 0
            time_sum = 0
            for result in results[f]:
                build_time_sum += result[0]
                time_sum += result[1]
            build_average = build_time_sum / float(iterations)
            average = time_sum / float(iterations)
            fid = function_identifiers[f]
            gap_result[fid] = average
            print "    {0}: {1} seconds ({2} seconds build time)".format(fid, average, build_average)
        gap_results[g] = gap_result

    print ""
    print "JSON results blob:"
    print json.dumps(gap_results)

