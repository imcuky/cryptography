
import random

def test_prime(n, t):
    
    # Factor n-1 as 2^k * q   
    k, q = 0, n - 1
    while q % 2 == 0:
        k += 1
        q //= 2
    

    # find a prime within 6 loop
    for _ in range(t):

        a = random.randint(1, n - 1)
        x = pow(a, q, n)
        
        # first property
        # a^2mod p = 1 if and only if either a mod p = 1 or a mod p = -1 (p = p - 1)
        if x == 1 or x == n - 1:

            return True

        for j in range(k):
            x = pow(a, pow(2,j)*q, n)

            # second property
            # a^(2^(j - 1)*q) mod p = -1 (p - 1)
            if x == n - 1:
                return True
            else:
                return False
    
    return False

    
# find a b-bit integer that is probably prime with t = 6
def miller_rabin(b):
    while True:
        # generate a random b-bit integer
        rand = random.randint(2**(b-1) + 1, 2**b)  
        # test prime under
        if test_prime(rand, 6):
            return rand

if __name__ == "__main__":
    for _ in range(5):
        print(f"Found a {15}-bit prime: {miller_rabin(15)}")
    
    print(f"The probable primes are in the table")