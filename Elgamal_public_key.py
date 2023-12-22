import random

# key generation
def generate_keys(q, alpha):
    # private
    x = random.randint(1, q - 1)
    # public
    y = pow(alpha, x, q)
    return x, y

# encryption
def encrypt(q, alpha, public_key, plaintext, k = -1):
    
    # random integer k
    if k == -1:
        k = random.randint(1, q - 1)
    
    # one-time key
    key = pow(public_key, k, q)
    c1 = pow(alpha, k, q)
    c2 = (plaintext * key) % q
    return c1, c2

# decryption
def decrypt(x, q, c1, c2):
    s = pow(c1, x, q)
    s_inv = pow(s, -1, q)
    plaintext = (c2 * s_inv) % q
    return plaintext

# find m2 given m1
def m2_give_m1(c22, q, alpha, m1, k):

    #C2,1 = C1,1
    #M2 = (C2,1)^-1 * C2,2 M1 mod q
    
    c1 = pow(alpha, k, q)
    mod_inverse = pow(c1,-1, q)
    m2 = pow(mod_inverse * c22 * m1, 1, q)
    
    return m2

if __name__ == "__main__":
    # public known

    q = 89
    # primitive root
    alpha = 13
    # random integer 
    k = 43
    # Key Generation
    private_key, public_key = generate_keys(q, alpha)

    # encryption
    plaintext = 62
    c1, c2 = encrypt(q, alpha, public_key, plaintext, -1)

    # decryption
    decrypted_plaintext = decrypt(private_key, q, c1, c2)


    print("Original plaintext:", plaintext)
    print("Decrypted plaintext:", decrypted_plaintext)

    # define c2,2 as 42, then find M2
    c22 = 42

    print("M1: ", plaintext)
    print("M2: ", m2_give_m1(c22, q, alpha, plaintext, k))
