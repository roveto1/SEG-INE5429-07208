import time
import numpy
import csv
import matplotlib.pyplot as plt
import os, math

from pseudo_number_gen.Xorshift import Xorshift
from pseudo_number_gen.LCG import LCG

def ns_to_ms(ns):
    return ns / 1_000_000
def to_superscript_10(n):
    exponent = int(math.log10(n))
    sup = str(exponent).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
    return f"10{sup}"

def plot_histogram(data, num_iterations, bins=100, title="Histogram", save_path=None):
    max_val = max(data)
    data = [x / max_val for x in data]  # normaliza para 0–1

    plt.hist(data, bins=bins, edgecolor='black', color="darkgreen", linewidth=0.25)
    plt.title(title)
    plt.xlabel("Normalized Numbers")
    plt.ylabel(f"Frequency over {to_superscript_10(num_iterations)} iterations")
    plt.grid(axis='y', linestyle='-', alpha=0.7)

    if save_path:
        # Cria diretório se não existir
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(f"{save_path}/{title}.png", dpi=300)  # dpi ajusta a resolução

    plt.close()

#plot_histogram(values, bin_count, f"Blum Blum Shub ({samples} números pseudo-aleatórios gerados)", f"Número Gerado [0, {max_value}]", "Frequência")
def test_lcg(NUM_SIZES, LCG_SEED, NUM_ITERATIONS, LCG_A, LCG_C):
    lcg_results = []

    for index, bits in enumerate(NUM_SIZES):
        lcg = LCG(seed=LCG_SEED, bits=bits, a=LCG_A, c=LCG_C)
        times = []
        rng = []
        for _ in range(NUM_ITERATIONS):
            start = time.perf_counter_ns()
            n = lcg.next()
            end = time.perf_counter_ns()
            times.append(end-start)
            rng.append(n)
        avg_ns = numpy.average(times)
        print(f"LCG {bits}-bit: {avg_ns} ns per iteration")
        print(min(rng).bit_length(), min(rng), max(rng).bit_length(), max(rng))
        plot_histogram(rng, NUM_ITERATIONS, 100, f"LCG {bits}b", "results/plots/LCG")

        lcg_results.append((index+1, bits, min(rng).bit_length(), min(rng), max(rng).bit_length(), max(rng), ns_to_ms(avg_ns)))

    with open("results/LCG_benchmark.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Bits", "MinBitSize", "MinRNG", "MaxBitSize", "MaxRNG", "AvgTime(ms)"])
        writer.writerows(lcg_results)

def test_xorshift(NUM_SIZES, XORSHIFT_SEED, NUM_ITERATIONS):
    xorshift_results = []

    for index, bits in enumerate(NUM_SIZES):
        xsh = Xorshift(state=XORSHIFT_SEED, bits=bits)
        times = []        
        rng = []
        for _ in range(NUM_ITERATIONS):
            start = time.perf_counter_ns()
            n = xsh.gen()
            end = time.perf_counter_ns()
            times.append(end-start)
            rng.append(n)
        avg_ns = numpy.average(times)
        print(f"Xorshift {bits}-bit: {avg_ns} ns per iteration")
        print(min(rng).bit_length(), min(rng), max(rng).bit_length(), max(rng))
        plot_histogram(rng, NUM_ITERATIONS, 100, f"Xorshift {bits}b", "results/plots/Xorshift")

        xorshift_results.append((index+1, bits, min(rng).bit_length(), min(rng), max(rng).bit_length(), max(rng), ns_to_ms(avg_ns)))

    with open("results/Xorshift_benchmark.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Bits", "MinBitSize", "MinRNG", "MaxBitSize", "MaxRNG", "AvgTime(ms)"])
        writer.writerows(xorshift_results)
def item2():
    NUM_SIZES = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    NUM_ITERATIONS = 1_000_000

    LCG_SEED = 2**33
    LCG_A = 3124199165 
    LCG_C = 27181987157
    test_lcg(NUM_SIZES, LCG_SEED, NUM_ITERATIONS, LCG_A, LCG_C)

    XORSHIFT_SEED = 2**33
    test_xorshift(NUM_SIZES, XORSHIFT_SEED, NUM_ITERATIONS)

    