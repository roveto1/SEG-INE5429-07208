import force_bit_size as cfg

class Xorshift:
    def __init__(self, state=2**33, bits=32):
        # Definições basicas do Xorshift
        self.state = state         # Estado inicial (seed) 
        self.bits = bits           # Quantidade de bits definida
        self.mask = (2**bits) - 1  # Máscara para garantir que o valor gerado esteja dentro do tamanho definido

    # Gera o próximo número na sequência
    def gen(self):
        # Algoritmo Xorshift
        self.state ^= (self.state << 13) & self.mask            # x = x ^ (x << 13) & mask
        self.state ^= (self.state >> 7) & self.mask             # x = x ^ (x >> 7) & mask
        self.state ^= (self.state << 17) & self.mask            # x = x ^ (x << 17) & mask

        self.state = self.state & self.mask                     # Garante que o valor gerado esteja dentro do tamanho definido

        if cfg.FORCE_BIT_SIZE:                                  # Para o relatório, FORCE_BIT_SIZE está como False
            self.state = self.state | ((1 << (self.bits - 1)))  # Força o bit mais significativo a ser 1, garantindo o tamanho definido

        return self.state                                       # Retorna o número gerado
    

    
