

class LCG:
    def __init__(self, seed=1, bits=32, a=33690453, c=1013904223):
        self.bits = bits
        self.m = 2**bits
        self.a = a 
        self.c = c 
        self.state = seed #% self.m

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state
