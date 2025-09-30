import time
import csv

from teste_primalidade import generate_prime_fermat, generate_prime_miller_rabin

def ns_to_ms(ns):
    return ns / 1_000_000
def item3():
    NUM_SIZES = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    INITIAL_SEED = 2**33

    with open("results/primes.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "PNGR", "Algorithm", "Bits", "Time(ms)", "Prime"])

        # --- LCG ---
        for idx, bits in enumerate(NUM_SIZES, start=1):
            # Miller-Rabin
            start = time.perf_counter_ns()
            p1 = generate_prime_miller_rabin(bits, "lcg", seed=INITIAL_SEED, k=5)
            end = time.perf_counter_ns()
            t1 = end - start
            t1 = ns_to_ms(t1)
            print(f"[LCG] Miller-Rabin {bits}-bit prime in {t1/1e3:.3f}s")
            writer.writerow([idx, "LCG", "Miller-Rabin", bits, t1, p1])

            # Fermat
            start = time.perf_counter_ns()
            p2 = generate_prime_fermat(bits, "lcg", seed=INITIAL_SEED, k=5)
            end = time.perf_counter_ns()
            t2 = end - start
            t2 = ns_to_ms(t2)
            print(f"[LCG] Fermat       {bits}-bit prime in {t2/1e3:.3f}s")
            writer.writerow([idx + len(NUM_SIZES), "LCG", "Fermat", bits, t2, p2])

        # --- Xorshift ---
        for idx, bits in enumerate(NUM_SIZES, start=1 + 2*len(NUM_SIZES)):
            # Miller-Rabin
            start = time.perf_counter_ns()
            p1 = generate_prime_miller_rabin(bits, "xorshift", seed=INITIAL_SEED, k=5)
            end = time.perf_counter_ns()
            t1 = end - start
            t1 = ns_to_ms(t1)
            print(f"[Xorshift] Miller-Rabin {bits}-bit prime in {t1/1e3:.3f}s")
            writer.writerow([idx, "Xorshift", "Miller-Rabin", bits, t1, p1])

            # Fermat
            start = time.perf_counter_ns()
            p2 = generate_prime_fermat(bits, "xorshift", seed=INITIAL_SEED, k=5)
            end = time.perf_counter_ns()
            t2 = end - start
            t2 = ns_to_ms(t2)
            print(f"[Xorshift] Fermat       {bits}-bit prime in {t2/1e3:.3f}s")
            writer.writerow([idx + len(NUM_SIZES), "Xorshift", "Fermat", bits, t2, p2])