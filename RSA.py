import time
from Miller_rabin import miller_rabin


# encryption
def encrypt(m, e, n):

    c = pow(m, e, n)

    return c
# decryption
def decrypt(c, d, n):

    m = pow(c, d, n)

    return m

# decryption with CRT
def decrypt_CRT(c, p, q, n, d):

    # Vp = Cd mod p Vq = Cdmod q
    v_p = pow(c, d, p)
    v_q = pow(c, d, q)

    # Xp = q * (q^-1mod p) Xq = p * (p^-1mod q)
    x_p = q * pow(q, -1, p)
    x_q = p * pow(p, -1, q)

    # M = (VpXp + VqXq) mod n
    m = pow(v_p * x_p + v_q * x_q, 1, n)

    return m

# Impliment the The RSA Algorithm
if __name__ == "__main__":

    e = 65537
    m = 476921883457909

    # use miller-rabin to find a 1024 bit prime
    p = miller_rabin(1024)
    q = miller_rabin(1024)

    n = p * q
    phi = (p-1)*(q-1)

    # d such that de = 1 (mod phi)
    d = pow(e, -1, phi)

    # cipertext
    c = encrypt(m, e, n)


    print(f"Message: {m}")


    start_time = time.time()
    m1 = decrypt(c, d, n)
    end_time = time.time()
    print(f"decrypt without CRT: {m1} with time {end_time - start_time} seconds")


    crt_start_time = time.time()
    m2 = decrypt_CRT(c, p, q, n, d)
    crt_end_time = time.time()
    print(f"decrypt with CRT: {m2} with time {crt_end_time - crt_start_time} seconds")
    