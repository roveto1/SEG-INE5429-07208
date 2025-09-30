import force_bit_size as cfg

class LCG:
    def __init__(self, seed=1, bits=32, a=3124199165, c=27181987157):
        # Definições basicas do LCG
        self.bits = bits            # Quantidade de bits definida
        self.m = 2**bits            # Definido como 2^bits, para não estrapolar o tamanho definido
        self.a = a                  # Multiplicador
        self.c = c                  # Incremento
        self.state = seed % self.m  # Estado inicial (seed), garantindo que esteja dentro do tamanho definido

    # Gera o próximo número na sequência
    def next(self):
        self.state = (self.a * self.state + self.c) % self.m    # Equação do LCG -> Xn+1 = (a * Xn + c) mod m. 
                                                                # State já é atualizado para o próximo número

        if cfg.FORCE_BIT_SIZE:                                  # Para o relatório, FORCE_BIT_SIZE está como False
            self.state = self.state | ((1 << (self.bits - 1)))  # Força o bit mais significativo a ser 1, garantindo o tamanho definido
            
        return self.state                                       # Retorna o número gerado





