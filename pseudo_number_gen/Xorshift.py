

class Xorshift:
    def __init__(self, state=21, bits=32):
        self.state = state
        self.bits = bits
        self.mask = (1 << bits) - 1

    def gen(self):
        self.state ^= (self.state << 13) & self.mask
        self.state ^= (self.state >> 17) & self.mask
        self.state ^= (self.state << 5) & self.mask
        return self.state & self.mask
