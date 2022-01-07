import random
import math
from fractions import Fraction
from numpy.compat import long


# efficient way to find the highest power of 2 that will divide a number using bit ops
def get_high_pow_2(number):
    return number & (~(number - 1))


# function that will perform modular exponentiation ie x^a mod p
def mod_exp(x, a, p):
    # init result
    result = 1

    # Update if x >= p
    x = x % p
    while a > 0:
        # If a is odd, multiply x with result
        if a & 1:
            result = (result * x) % p

        # y must be even now
        a = a >> 1
        x = (x * x) % p

    return result


# method that will perform the miller rabin primality test
# note that I run 40 iterations under the assumption that 40 iterations makes it sufficiently probable that the
# random number is indeed prime and that running after this until failure could give an adversary
# time to crack one of the keys
def miller_rabin(candidate):
    # miller rabin dictates that the candidate must be candidate > 2 and odd
    # still return true for n = 2
    if candidate == 2:
        return True
    if candidate % 2 == 0 or candidate < 2:
        return False

    # write the candidate-1 as 2^s*q with q odd
    sub_one = candidate - 1
    pow_2 = get_high_pow_2(sub_one)
    s = long(math.log2(pow_2))
    # note that here the conversion to Fraction is necessary in order for the division of extremely
    # large numbers to be performed correctly
    q = long(Fraction(sub_one) / Fraction(pow_2))

    assert (2 ** s * q == sub_one)

    # perform 40 iterations
    for i in range(40):
        # pick a randomly in the range from [2,candidate-1]
        a = random.randint(2, sub_one)
        x = mod_exp(a, q, candidate)
        if x == 1 or x == sub_one:
            continue

        for j in range(s - 1):
            x = mod_exp(x, 2, candidate)
            # note that in my implementation false corresponds to composite label
            if x == 1:
                return False
            if x == sub_one:
                break
        else:
            return False
    # label probably prime if it passes all rounds
    return True


class PrimeGenerator:
    # creating a prime generator that will generate randoms of the specified number of bits
    # note that I have the default bits=512 so that n = p*q would be around 1024 bits
    def __init__(self, bits=512):
        self.bits = bits

    # method that will generate a random large number
    def generate_candidate(self):
        # generate a candidate of the desired number of bits
        return random.getrandbits(self.bits)

    # method that will get a random prime of the specified number of bits
    def generate_prime(self):
        # generate specified bit length candidates until a prime is obtained
        while True:
            potential_prime = self.generate_candidate()

            if miller_rabin(potential_prime):
                break
        return potential_prime
