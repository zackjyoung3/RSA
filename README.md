Last semester I took a number theory and cryptograhpy course and was fascinated behind the mathematical basis behind different encryption algorithms. For this
project I wanted to create an implementation of RSA cryptosystem that I had learned.

The first step in RSA is to generate primes p and q and letting n = p*q. For my implementation I created two different means of obtaining the primes. Either the 
user could enter in primes less than 100,000 for an example demonstration or an instance of the PrimeGenerator class would be used to obtain 2 512 bit primes
to form approximately 1024 bit n.
- for user entered primes, an instance of the Sieve class is created that contains an array where primes are marked with 1 and non primes with 0 using the 
sieve of eratosthenes algorithm. Thus, when user enters input, it is an O(1) op to check whether the inputted number is prime. Note that I encode and decode
using the ASCII value for chars and thus, it must be that n > 256 when computed using the user's p and q
- for the random prime generation, the instance of the PrimeGenerator has the default value for bits of 512, and generates candidate 512 bit random numbers until 
the candidate passes 40 rounds of the Miller-Rabin primality test making it sufficiently probable that the random number is indeed prime and note that running
that running after this until failure could give an adversary time to crack one of the keys

Then, phi(n) is computed using the beautiful number theory behind Euler's totient function

(1) given prime a, phi(a) = (a-1)

(2) given a,b coprime phi(a*b) = phi(a)*phi(b)

- since n = p*q => phi(n) = phi(p*q) = phi(p)*phi(q) from (2)
- since p,q prime => phi(p)*phi(q) = (p-1)(q-1)

Thus, phi(n) = (p-1)(q-1)

Then, e is selected such that gcd(e,phi(n)) = 1
- for my implementation I randomly select e from a list of common e values until gcd(e,phi(n)) = 1
- gcd(e,phi(n)) = 1 is checked using the extended Euclidean algorithm which in my implementation also returns the gcd as a linear combination
Thus, after running the extended Euclidean to confirm, gcd will be equal to 1 will be returned and s and t will be returned such that 

s *phi(n) + t *e = 1(gcd)

(taking mod phi(n) of both sides obtain)

d*e (congruent) = 1 mod phi(n)

d is the multiplicative inverse of e mod phi(n) and is kept private

e and n are made public
Note that in my implementation I used the mod library because I found that it worked best with numbers of incredibly large length that would be generated in my 
random prime generateion version of my implementation of RSA
public_key = Mod(e, n) makes it so that a ** public_key = a^e mod n
private_key = Mod(d, n) makes it so that a ** private_key = a^d mod n, exactly as required

For encryption, I take the user's input and encode character by character using the public_key and ascii value of the character
to form a list where each element of the list corresponds to the encoded character from the user's input
Then, in decryption I decode from the encrypted list using the private_key and obtain each character from the ascii value obtained from decryption.

Note that the encryption and decryption work because Euler's Theorem which is a generalization of Fermat's little theorem

Euler's Theorem: given a,n coprime, a^(phi(n)) (congruent)= 1 mod n

(a) d*e (congruent) = 1 phi(n) => since d and e are positive d*e = 1 + q*phi(n) for some positive int q

To Show: after encryption and decryption, the correct original message is obtained ie m^(e*d) (congruent)= m mod n
- m^(e*d) = m^(1 + q*phi(n)) (from a)
- m^(1 + q*phi(n)) = m*m^(q*phi(n)) = m*(m^(phi(n))^q
- m*(m^(phi(n))^q (congruent)= m*1^q (from Euler's) (congruent)= m mod n
 
Therefore, m^(e*d) (congruent)= m mod n as required



