"""
Primalidade com Miller-Rabin + Fermat
"""

from pseudo_number_gen.LCG import LCG
from pseudo_number_gen.Xorshift import Xorshift


# ======================================================
# Funções auxiliares para usar PRNG
# ======================================================
def randbits(bits: int, algo: str = "lcg", last_value: int = 21) -> tuple[int, int]:
    """
    Gera um inteiro de 'bits' bits usando o algoritmo especificado.
    Usa o último valor gerado como semente/estado para continuar a sequência.

    Retorna:
        (novo_valor, novo_last_value)
    """
    if algo.lower() == "lcg":
        prng = LCG(seed=last_value, bits=bits, a=1664525, c=1013904223)
        value = prng.next()
        return value & ((1 << bits) - 1), value

    elif algo.lower() == "xorshift":
        prng = Xorshift(state=last_value, bits=bits)
        value = prng.gen()
        return value & ((1 << bits) - 1), value

    else:
        raise ValueError("Algoritmo não suportado. Use 'lcg' ou 'xorshift'.")

def randrange_custom(low: int, high: int, algo: str, last_value: int) -> tuple[int, int]:
    """
    Mimics random.randint(low, high) using the custom randbits function.
    Returns (number, new_last_value).
    """
    if low > high:
        raise ValueError("low must be <= high")

    # Range size
    rng = high - low + 1

    # Generate enough bits to cover the range
    bits = rng.bit_length()
    while True:
        val, last_value = randbits(bits, algo, last_value)
        if val < rng:  # accept only if within range
            return low + val, last_value

def normalize_candidate(n: int, bits: int) -> int:
    """Garante que n tenha exatamente 'bits' bits, MSB=1 e LSB=1."""
    n |= (1 << (bits - 1))  # força bit mais alto
    n |= 1                  # força ser ímpar
    return n & ((1 << bits) - 1)

def power(a: int, n: int, p: int) -> int:
    """Iterative modular exponentiation: (a^n) % p."""
    res = 1
    a = a % p

    while n > 0:
        if n % 2:  # if n is odd
            res = (res * a) % p
            n -= 1
        else:
            a = (a * a) % p
            n //= 2

    return res % p

# ======================================================
# Testes de primalidade
# ======================================================
def miller_test(d: int, n: int, algo: str, last_value: int) -> tuple[bool, int]:
    """
    One Miller-Rabin trial. Returns (probably_prime, new_last_value).
    """
    # Pick a random base in [2..n-2]
    a, last_value = randrange_custom(2, n - 2, algo, last_value)

    # Compute a^d % n
    x = power(a, d, n)

    if x == 1 or x == n - 1:
        return True, last_value

    # Keep squaring x until d reaches n-1
    while d != n - 1:
        x = (x * x) % n
        d *= 2

        if x == 1:
            return False, last_value
        if x == n - 1:
            return True, last_value

    return False, last_value

def miller_rabin(n: int, k: int, algo: str, last_value: int) -> tuple[bool, int]:
    """Miller-Rabin primality test with custom PRNG."""
    # Corner cases
    if n <= 1 or n == 4:
        return False, last_value
    if n <= 3:
        return True, last_value

    # Write n-1 as d*2^r with d odd
    d = n - 1
    while d % 2 == 0:
        d //= 2

    # Run k trials
    for _ in range(k):
        ok, last_value = miller_test(d, n, algo, last_value)
        if not ok:
            return False, last_value

    return True, last_value

def fermat_test(n: int, k: int, algo: str, last_value: int) -> tuple[bool, int]:
    """Fermat primality test with custom PRNG for base selection."""
    if n in (1, 4):
        return False, last_value
    if n in (2, 3):
        return True, last_value
    if n % 2 == 0:
        return False, last_value

    for _ in range(k):
        # Use custom randint replacement: [2, n-2]
        a, last_value = randrange_custom(2, n - 2, algo, last_value)

        # Fermat's Little Theorem check
        if power(a, n - 1, n) != 1:
            return False, last_value

    return True, last_value


# ======================================================
# Geração de primos a partir do PRNG
# ======================================================
def generate_prime_miller_rabin(bits: int, algo: str = "lcg", seed: int = 21, k: int = 8) -> int:
    """Gera um número primo de 'bits' bits usando Miller-Rabin."""
    last_value = seed
    while True:
        candidate, last_value = randbits(bits, algo, last_value)
        candidate = normalize_candidate(candidate, bits)
        ok, last_value = miller_rabin(candidate, k, algo, last_value)
        if not ok:
            print("X", end="", flush=True)
        else:
            print("O")
            return candidate


def generate_prime_fermat(bits: int, algo: str = "lcg", seed: int = 21, k: int = 8) -> int:
    """Gera um número primo de 'bits' bits usando Fermat."""
    last_value = seed
    while True:
        candidate, last_value = randbits(bits, algo, last_value)
        candidate = normalize_candidate(candidate, bits)
        ok, last_value = fermat_test(candidate, k, algo, last_value)
        
        if not ok:
            print("X", end="", flush=True)
        else:
            print("O")
            return candidate