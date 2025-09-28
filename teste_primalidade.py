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


def normalize_candidate(n: int, bits: int) -> int:
    """Garante que n tenha exatamente 'bits' bits, MSB=1 e LSB=1."""
    n |= (1 << (bits - 1))  # força bit mais alto
    n |= 1                  # força ser ímpar
    return n & ((1 << bits) - 1)


# ======================================================
# Testes de primalidade
# ======================================================
def miller_rabin(n: int, k: int, algo: str, last_value: int) -> tuple[bool, int]:
    """Teste de Miller-Rabin usando PRNG para gerar bases."""
    if n < 2:
        return False, last_value
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n == p:
            return True, last_value
        if n % p == 0:
            return False, last_value

    # escreve n-1 = 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a, last_value = randbits(n.bit_length(), algo, last_value)
        a = 2 + (a % (n - 3))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break
        if composite:
            return False, last_value
    return True, last_value


def fermat_test(n: int, k: int, algo: str, last_value: int) -> tuple[bool, int]:
    """Teste de Fermat usando PRNG para escolher bases."""
    if n < 2:
        return False, last_value
    if n in (2, 3):
        return True, last_value
    if n % 2 == 0:
        return False, last_value

    for _ in range(k):
        a, last_value = randbits(n.bit_length(), algo, last_value)
        a = 2 + (a % (n - 3))
        if pow(a, n - 1, n) != 1:
            return False, last_value
    return True, last_value


# ======================================================
# Geração de primos a partir do PRNG
# ======================================================
def generate_prime_miller_rabin(bits: int, algo: str = "lcg", k: int = 8) -> int:
    """Gera um número primo de 'bits' bits usando Miller-Rabin."""
    last_value = bits
    while True:
        candidate, last_value = randbits(bits, algo, last_value)
        candidate = normalize_candidate(candidate, bits)
        ok, last_value = miller_rabin(candidate, k, algo, last_value)
        if not ok:
            print("X", end="", flush=True)
        else:
            print("O")
            return candidate


def generate_prime_fermat(bits: int, algo: str = "lcg", k: int = 8) -> int:
    """Gera um número primo de 'bits' bits usando Fermat."""
    last_value = bits
    while True:
        candidate, last_value = randbits(bits, algo, last_value)
        candidate = normalize_candidate(candidate, bits)
        ok, last_value = fermat_test(candidate, k, algo, last_value)
        
        if not ok:
            print("X", end="", flush=True)
        else:
            print("O")
            return candidate