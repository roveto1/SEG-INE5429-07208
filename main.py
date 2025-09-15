import time
import numpy
import csv

from pseudo_number_gen.Xorshift import Xorshift
from pseudo_number_gen.LCG import LCG

if __name__ == "__main__":

    NUM_SIZES = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    LCG_SEED = 21
    NUM_ITERATIONS = 10_000_000

    LCG_A = 1664525
    LCG_C = 1013904223

    lcg_results = []

    for index, bits in enumerate(NUM_SIZES):
        lcg = LCG(seed=LCG_SEED, bits=bits, a=LCG_A, c=LCG_C)
        times = []
        for _ in range(NUM_ITERATIONS):
            start = time.perf_counter_ns()
            lcg.next()
            end = time.perf_counter_ns()
            times.append(end-start)
        avg_ns = numpy.average(times)
        print(f"LCG {bits}-bit: {avg_ns} ns per iteration")

        lcg_results.append((index+1, bits, avg_ns))

    with open("results/LCG_benchmark.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Bits", "Time(ns)"])
        writer.writerows(lcg_results)

    XORSHIFT_SEED = 21

    xorshift_results = []

    for index, bits in enumerate(NUM_SIZES):
        xsh = Xorshift(state=XORSHIFT_SEED, bits=bits)
        times = []
        
        for _ in range(NUM_ITERATIONS):
            start = time.perf_counter_ns()
            xsh.gen()
            end = time.perf_counter_ns()
            times.append(end-start)
        avg_ns = numpy.average(times)
        print(f"Xorshift {bits}-bit: {avg_ns} ns per iteration")

        xorshift_results.append((index + 1, bits, avg_ns))

    with open("results/Xorshift_benchmark.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Bits", "Time(ns)"])
        writer.writerows(xorshift_results)