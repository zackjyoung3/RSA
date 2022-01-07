import random

from Sieve import Sieve
from PrimeGenerator import PrimeGenerator, miller_rabin, mod_exp
import numpy as np
from fractions import Fraction
from mod import Mod


#
# def miller_rabin_check():
#     primes = {}
#     for i in range(2, 1000):
#         if miller_rabin(i):
#             primes[str(i)] = True
#
#     counter = 0
#     for prime in primes:
#         print(prime)
#         counter += 1
#     print(counter)

# method that will perform the extended euclidean algorithm for a and b
# at the end will return the gcd as a linear combination of a and b ie
# s*a + t*b = d where d is the gcd(a,b)
def extended_euclidean(a, b):
    if b == 0:
        gcd, s, t = a, 1, 0
        return gcd, s, t
    else:
        s2, t2, s1, t1 = 1, 0, 0, 1
        while b > 0:
            q = a // b
            r, s, t = (a - b * q), (s2 - q * s1), (t2 - q * t1)
            a, b, s2, t2, s1, t1 = b, r, s1, t1, s, t
        gcd, s, t = a, s2, t2
        return gcd, s, t


# method for RSA with random p and q generating n around 1024 bits
def RSA_random():
    # common values for e are 3, 5, 17, 257, 65537
    common_e_vals = [3, 5, 17, 257, 65537]
    # select random e from common e values
    e_index = random.randint(0, 4)
    e = common_e_vals[e_index]

    # generate random 512 bit primes p and q
    generator = PrimeGenerator()

    # generate candidates for n until a valid n is obtained
    while True:
        # since e is an odd prime, can do the less computationally expensive test
        while True:
            p = generator.generate_prime()
            if p % e != 1:
                break

        while True:
            q = generator.generate_prime()
            if q % e != 1:
                break

        # n is p*q
        n = p * q

        # phi(n) = phi(p)*phi(q) p and q are prime => phi(n) = phi(p)*phi(q) = (p-1)(q-1)
        phi_n = (p - 1) * (q - 1)

        gcd, s, t = extended_euclidean(phi_n, e)
        if gcd == 1:
            break

    # at this point have s*phi(n) + t*e = 1
    # take mod phi(n) both sides to obtain d*e = 1 mod phi(n) ie to find d, the inverse of e mod phi(n)
    d = t % phi_n

    print('d*e (congruent)=', (d * e) % phi_n, 'mod phi(n)')

    # publish e and n
    print('e is:', e)
    print('n is:', n)

    # create the public and private keys using Mod because the numbers are so large
    public_key = Mod(e, n)
    private_key = Mod(d, n)
    return public_key, private_key, n


# method that will encrypt a user's message
def encrypt(public_key):
    # prompt the user to enter a message
    message = input('Please enter the message that you would like to encrypt or quit to end session:')

    # user wants to end the session
    if message == 'quit':
        return message

    # encrypt the message by finding the ascii equiv of the char and performing ascii_equiv^e mod
    # n to obtain encoded_char, storing the encoded message as a list
    encoded = []
    for message_char in message:
        ascii_equiv = ord(message_char)
        encoded_char = ascii_equiv ** public_key
        encoded.append(encoded_char)

    # print the encoded message and return it
    print('Encoded:', encoded)
    return encoded


# method that will decrypt code text
def decrypt(encoded, private_key):
    # decrypt each character that has been encoded to form the decrypted message
    decrypted = ""
    for encoded_char in encoded:
        ascii_char = encoded_char ** private_key
        decrypted += chr(int(ascii_char))

    # print the decrypted message
    print('Decrypted:', decrypted)
    return decrypted


# method for a session using rsa encryption
def session(public_key, private_key):
    print('Session with RSA started...')
    while True:
        encoded = encrypt(public_key)
        if encoded == 'quit':
            break
        decrypt(encoded, private_key)


# method that will enable the user to enter their own p and q for rsa
def RSA_user():
    # instantiation of the Sieve class that will have an numpy array with marked primes/non primes
    # permitting O(1) lookup to determine whether or not the number entered is prime
    sieve_prime_test = Sieve()
    # let the user know that the n obtained must be at least 256 for decryption purposes
    print('Note: p,q values must be such that n=p*q > 256 due to ascii conversion!!!')

    # obtain input until a valid state for RSA is generated
    while True:
        while True:
            p = input('Please enter a prime p less than 100,000:')
            try:
                p = int(p)
            except ValueError:
                print('The value entered could not be converted to an int')
                continue
            if p >= 100000:
                print('Prime entered must be less than 100,000!')
                continue
            if sieve_prime_test.is_prime(p):
                break

            print('the number entered was not a prime')

        while True:
            q = input('Please enter a prime q less than 100,000:')
            try:
                q = int(q)
            except ValueError:
                print('The value entered could not be converted to an int')
                continue

            if q >= 100000:
                print('Prime entered must be less than 100,000!')
                continue
            if sieve_prime_test.is_prime(q):
                break
            print('the number entered was not a prime')

        # n is p*q
        n = p * q
        if n < 256:
            print('Error! p,q values must be such that n=p*q > 256 due to ascii conversion')
            continue

        # phi(n) = phi(p)*phi(q) p and q are prime => phi(n) = phi(p)*phi(q) = (p-1)(q-1)
        phi_n = (p - 1) * (q - 1)

        # common values for e are 3, 5, 17, 257, 65537
        common_e_vals = [3, 5, 17, 257, 65537]
        while True:
            # select random e from common e values
            e_index = random.randint(0, 4)
            e = common_e_vals[e_index]
            if e < phi_n:
                break

        gcd, s, t = extended_euclidean(phi_n, e)
        if gcd == 1:
            break
        print('gcd(e, phi(n)) != 1')

    # at this point have s*phi(n) + t*e = 1
    # take mod phi(n) both sides to obtain d*e = 1 mod phi(n) ie to find d, the inverse of e mod phi(n)
    d = t % phi_n

    print('d*e (congruent)=', (d * e) % phi_n, 'mod phi(n)')

    # publish e and n
    print('e is:', e)
    print('n is:', n)

    # create the public and private keys using Mod because the numbers are so large
    public_key = Mod(e, n)
    private_key = Mod(d, n)
    return public_key, private_key, n


# method that will run the correct version of RSA as specified by the user
def RSA():
    while True:
        option = input("Please enter either user to enter your own "
                       "experimental p,q for RSA or random for random 512 bit p,q:")
        if option == 'user' or option == 'random':
            break
        print('Error! Must enter \'user\' or \'random\'!')

    # run the correct version of RSA
    if option == 'user':
        public_key, private_key, n = RSA_user()

    if option == 'random':
        public_key, private_key, n = RSA_random()

    session(public_key, private_key)


# main
if __name__ == '__main__':
    RSA()
