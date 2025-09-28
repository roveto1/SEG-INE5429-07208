import math

n_bits = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
a = 31792125

c = 12345

for i in n_bits:
    print(f"a < 2^{i}: {a < 2**i}")
    print(f"c < 2^{i}: {c < 2**i}")
    m = 1 << i
    m1 = 2**i
    print(f"m = {m}")
    print(f"m1 = {m1}")
    print(m == m1)

    print(f"\nVerificando para m = 2^{i} ({m}):")

    # Regra 1: m e c coprimos
    if math.gcd(c, m) != 1:
        print(" ❌ Regra 1 falhou (m e c não são coprimos)")
        continue
    else:
        print(" ✅ Regra 1 ok (m e c são coprimos)")

    # Regra 2: a - 1 divisível por todos fatores primos de m (só 2 no caso)
    if (a - 1) % 2 != 0:
        print(" ❌ Regra 2 falhou (a - 1 não é divisível por 2)")
        continue
    else:
        print(" ✅ Regra 2 ok (a - 1 divisível por 2)")

    # Regra 3: se m divisível por 4, então (a - 1) divisível por 4
    if m % 4 == 0 and (a - 1) % 4 != 0:
        print(" ❌ Regra 3 falhou (a - 1 não é divisível por 4)")
    else:
        print(" ✅ Regra 3 ok (a - 1 divisível por 4 quando necessário)")