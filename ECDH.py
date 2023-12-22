from random import randint, random
import time
from Miller_rabin import miller_rabin
from fractions import Fraction

# impliment P+Q
def add_point(P, Q, a, p, n = 1):

    P_1 = P
    Q_1 = Q

    for _ in range(n):

        x_p = P_1[0]
        y_p = P_1[1]

        x_q = Q_1[0]
        y_q = Q_1[1]

        if P_1 == Q_1:
            
            simplified_fraction = Fraction(3 * x_p**2 + a, 2 * y_p).limit_denominator()

            lamb = (simplified_fraction.numerator) % p * pow(simplified_fraction.denominator, -1, p)

        else:
            simplified_fraction = Fraction(y_q - y_p, x_q - x_p).limit_denominator()
            lamb =  (simplified_fraction.numerator) % p * pow(simplified_fraction.denominator, -1, p)
 
        # xR = (lamb^2 - xP - xQ) mod p
        x_r = (lamb**2 - x_p - x_q) % p

        # yR = (l*(xP - xR) - yP) mod p
        y_r = (lamb*(x_p - x_r) - y_p) % p

        R = (x_r, y_r)

        P_1 = R

    
    return P_1

# impliment n*p
def multiple_point(P, a, p, n):

    return add_point(P, P, a, p, n-1)


def find_order(G, a, p):
    
    current_point = G
    order = 1

    # if reach an error means find the point of infinity
    try:
        while True:
            k = add_point(current_point, G, a, p)
            order += 1
            current_point = k

    except Exception as e:
        return order - 1


def is_primitive_root(g, p):
    mod = list()
    # power from 1 to p-1
    for k in range(1, p):
        root = pow(g, k, p)
        if root in mod:
            return False
        mod.append(root)
    return True

def find_primitive_root(p):
    # 2 to p-1
    for g in range(2, p):
        # test if the current is a generator
        if is_primitive_root(g, p):
            return g
    return None

#size of public key is 1024 bits, size of private key is 160 bit
def DH(alpha, q):

    x_a = randint(1, q-1)
    y_a = pow(alpha, x_a, q)

    x_b = randint(1, q-1)
    y_b = pow(alpha, x_b, q)


    return y_a, y_b

if __name__ == "__main__":


    # use miller-rabin to find a 160 bit prime
    p = miller_rabin(160)

    a = 0

    b = -4

    # a point on this curve
    G = (2,2)

    n = find_order(G, a, p)

    # private key
    n_a = randint(1, n-1)
    n_b = randint(1, n-1)

    # public key
    P_a = multiple_point(G, a, p, n_a)
    P_b = multiple_point(G, a, p, n_b)
    
    # Secret Key
    start_time = time.time()
    k_a = multiple_point(P_b, a, p, n_a)
    k_b = multiple_point(P_a, a, p, n_b)
    end_time = time.time()

    if k_a == k_b:

        print(f"Find the shared secret with ECDH: {k_a} with time {end_time - start_time} seconds")

    # D-H at the same security level need a 1024 bit public key
    q = miller_rabin(1024)
    alpha = find_primitive_root(q)
    start_time = time.time()
    y_a, y_b = DH(alpha, q)
    end_time = time.time()

    if y_a == y_b:
        print(f"Find the shared secret DH: {y_a} with time {end_time - start_time} seconds")

