import hashlib
import random
import sympy
from fractions import Fraction


def signing(message, p, q, g, x, k):

    # Calculate r = (g^k mod p) mod q
    r = pow(g, k, p) % q

    # Calculate s = k^(-1) * (SHA-1(message) + x*r) mod q
    sha1_hash = int(hashlib.sha1(message.encode()).hexdigest(), 16)
    k_inv = pow(k, -1, q)
    s = (k_inv * (sha1_hash + x * r)) % q

    return r, s

def verifying(message, r, s, p, q, g, y):
    # Calculate w = s^(-1) mod q
    w = pow(s, -1, q)

    # Calculate u1 = (SHA-1(message) * w) mod q
    sha1_hash = int(hashlib.sha1(message.encode()).hexdigest(), 16)
    u1 = (sha1_hash * w) % q

    # Calculate u2 = r * w mod q
    u2 = (r * w) % q

    # Calculate v = ((g^u1 * y^u2) mod p) mod q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q

    # Verify the signature
    return v == r



if __name__ == "__main__":
    #==Global Public-Key Components==
    '''
    q = sympy.randprime(2**159, 2**160)

    # Generate 1024-bit prime p such that (p-1) is a multiple of q
    p = sympy.randprime(2**1023, 2**1024)
    while (p - 1) % q != 0:
        p = sympy.randprime(2**1023, 2**1024)
    '''

    # Use a predefined DSA parameters from NIST
    p = int("800000000000000089e1855218a0e7dac38136ffafa72eda7"
              "859f2171e25e65eac698c1702578b07dc2a1076da241c76c6"
              "2d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebe"
              "ac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2"
              "b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc87"
              "1a584471bb1", 16)

    q = int("f4f47f05794b256174bba6e9b396a7707e563c5b", 16)

    print((p - 1) % q == 0)
    # Find a generator g for the q-order subgroup of Zp*
    h = random.randint(1, p - 1)

    # g = h^((p - 1)/q) mod p,
    g = pow(h, (p-1)//q, p)

    #==User’s key pair==
    x = random.randint(0, q) #private
    y = pow(g, x, p) #public

    #==User’s Per-Message Secret Number==
    k = random.randint(0, q)

    message = "582346829557612"

    r, s = signing(message, p, q, g, x, k)

    # Verify the signature
    result = verifying(message, r, s, p, q, g, y)

    # Display results

    print("DSA public parameters: p = {}, q = {}, g = {}".format(p, q, g))
    print("\nMessage:", message)
    print("Public key (y):", y)
    print("Signature (r, s):", r, s)
    print("\nVerification result:", result)


    # Question 3
    print("\nUniqueness of k")

    # Sign the second message using the same k
    message2 = "8161474912583"
    r2, s2 = signing(message2, p, q, g, x, k)

    print("\nAttacker side:")

    # find k from s1, s2, m1, and m2
    m1_hash = int(hashlib.sha1(message.encode()).hexdigest(), 16)
    m2_hash = int(hashlib.sha1(message2.encode()).hexdigest(), 16)
    fraction1 = Fraction( m1_hash-m2_hash, s-s2)
    k_find = ((fraction1.numerator % q) * pow(fraction1.denominator, -1, q)) % q

    print("\nFind k: ", k_find, "; match orginal k?: ", k_find == k)

    # Calculate the compromised private key x
    fraction2 = Fraction( k * s - m1_hash, r)
    compromised_x = ((fraction2.numerator % q) * pow(fraction2.denominator, -1, q)) % q

    # Display results
    print("\nOriginal private key (x):", x)
    print("Compromised private key:", compromised_x)

    if x == compromised_x:
        print("By using the same k, the attacker can find the private key")
