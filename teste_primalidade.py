"""
Primalidade com Miller-Rabin + Fermat
"""

from pseudo_number_gen.LCG import LCG
from pseudo_number_gen.Xorshift import Xorshift
import csv


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
        prng = LCG(seed=last_value, bits=bits)
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
    # Escolhe uma base aleatória a no intervalo [2..n-2].
    # Aqui 'last_value' funciona como a seed para o gerador randrange_custom.
    a, last_value = randrange_custom(2, n - 2, algo, last_value)

    # Calcula x = a^d mod n.
    # Esse é o primeiro teste: se o resultado for 1 ou n-1,
    # n passa na rodada de Miller-Rabin para a base escolhida.
    x = power(a, d, n)

    if x == 1 or x == n - 1:
        return True, last_value

    # Caso contrário, inicia-se a sequência de quadraturas:
    # repete-se x = x^2 mod n e dobra-se o expoente d até atingir n-1.
    while d != n - 1:
        x = (x * x) % n
        d *= 2

        # Se em algum momento o resultado for 1, n é composto.
        if x == 1:
            return False, last_value
        # Se em algum momento o resultado for n-1, n passa no teste.
        if x == n - 1:
            return True, last_value

    # Se a sequência termina sem encontrar n-1, n é composto.
    return False, last_value

def miller_rabin(n: int, k: int, algo: str, last_value: int) -> tuple[bool, int]:
    # Casos triviais:
    # Se n <= 1 ou n == 4, retorna falso (composto).
    if n <= 1 or n == 4:
        return False, last_value
    # Se n <= 3, retorna verdadeiro (primo).
    if n <= 3:
        return True, last_value

    # Escreve n-1 na forma d*2^r, com d ímpar.
    # Isso é feito dividindo n-1 por 2 repetidamente até d ser ímpar.
    d = n - 1
    while d % 2 == 0:
        d //= 2

    # Executa k rodadas do teste de Miller-Rabin.
    # Em cada rodada, escolhe-se uma nova base aleatória
    # e aplica-se miller_test.
    for _ in range(k):
        ok, last_value = miller_test(d, n, algo, last_value)
        # Se alguma rodada detectar que n é composto, retorna imediatamente.
        if not ok:
            return False, last_value

    # Se todas as k rodadas passarem, n é considerado primo provável.
    return True, last_value

def fermat_test(n: int, k: int, algo: str, last_value: int) -> tuple[bool, int]:
    # Casos triviais: 1 e 4 são compostos
    if n in (1, 4):
        return False, last_value
    # 2 e 3 são primos
    if n in (2, 3):
        return True, last_value
    # Números pares maiores que 2 são compostos
    if n % 2 == 0:
        return False, last_value

    # Realiza k rodadas do teste para aumentar a confiabilidade
    for _ in range(k):
        # Escolhe uma base aleatória a no intervalo [2, n-2]
        # 'last_value' é usado como seed de randrange_custom
        a, last_value = randrange_custom(2, n - 2, algo, last_value)

        # Verifica a condição de Fermat: a^(n-1) ≡ 1 mod n
        # Se não for satisfeito, n é composto, e a é testemunha da composição
        if power(a, n - 1, n) != 1:
            return False, last_value

    # Se todas as rodadas passarem, n é considerado primo provável
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
        
if __name__ == "__main__":
    fermat_pseudoprimes = [
    341, 561, 645, 1105, 1387, 1729, 1905, 2047, 2465, 2701,
    2821, 3277, 4033, 4369, 4371, 4681, 5461, 6601, 7957, 8321,
    8481, 8911, 10585, 15841, 29341, 42799, 49141, 52633, 65281, 74665,
    80581, 85489, 88357, 90751, 253809, 334153, 340561, 399001, 410041, 449065
]
    # Lista para armazenar apenas resultados diferentes
    differing_results = []

    for fp in fermat_pseudoprimes:
        ok_m, _ = miller_rabin(fp, 5, "lcg", 2**33)
        result_m = "Primo provável" if ok_m else "Composto"
        ok_p, _ = fermat_test(fp, 5, "lcg", 2**33)
        result_p = "Primo provável" if ok_p else "Composto"

        # Armazena apenas se houver diferença
        if ok_m != ok_p:
            differing_results.append([fp, result_m, result_p])
            print(f"[Miller] PseudoPrime {fp}: {result_m}")
            print(f"[Fermat] PseudoPrime {fp}: {result_p}")

    # Exporta para CSV apenas os diferentes
    with open("differing_results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["PseudoPrime", "Miller-Rabin", "Fermat"])
        writer.writerows(differing_results)

    print("Resultados divergentes exportados para differing_results.csv")
