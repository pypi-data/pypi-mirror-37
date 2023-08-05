import math

def sine_encode(pos, i, d):
    return math.sin((pos / 10000.0 ** ((2*i) / d)
