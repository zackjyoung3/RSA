import numpy as np


class Sieve:
    # method that will init Sieve
    def __init__(self, primes_under=100000):
        self.primes_under = primes_under
        self.primes = np.ones(primes_under)
        self.fill_sieve()
        self.num_primes = 0
        self.get_num_primes()

    # method that will find all primes less that primes under using sieve method
    # note that I use 1 to denote that a number is prime and 0 to denote not a prime
    def fill_sieve(self):
        # mark that 0 and 1 are not primes
        self.primes[0] = 0
        self.primes[1] = 0

        current = 2
        while current*current < self.primes_under:
            # if current is not divisible by the previous primes obtained, we have found a new prime
            if self.primes[current] == 1:
                i = 0
                # mark off all multiples of the prime because they themselves cannot be prime
                while current*current+i*current < self.primes_under:
                    self.primes[current*current+i*current] = 0
                    i += 1
            # increment in both cases if current was prime or
            # current was divisible by a previous prime and thus cannot be prime itself
            current += 1

    def get_num_primes(self):
        # all primes are marked by 1
        for i in range(2, self.primes_under):
            if self.primes[i]:
                self.num_primes += 1

    # method that will return the number of primes that were found
    def primes_obtained(self):
        print(self.num_primes)

    # method that will determine if a number is prime from quick lookup
    def is_prime(self, num):
        if num > self.primes_under:
            return None
        return self.primes[num] == 1
