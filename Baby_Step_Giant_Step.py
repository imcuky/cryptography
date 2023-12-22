from DSA import signing, verifying


# apply Baby Step/Giant Step Algorithm
# solve a^x = b mod n
def baby_step_giant_step(a, b, n):
    '''
    
        for number a^n and b*a^(-mk)

        if a^n = ba^(-mk) mod N
        then
        a^(mk+n) = b mod N
    
    '''
    # random k value
    k = 5

    # Baby step: precompute a table of g^j mod p for j in [1, m)
    baby_steps = {pow(g, j, n): j for j in range(1,k-1)}

    r = 1

    # find a r such that a * b^(-k * r) mod p in baby step
    
    while r * k < n:

        giant_step = (pow(a, -k * r, n) * b) % n

        if giant_step in baby_steps:
            
            # find x
            return k * r + baby_steps[giant_step]

        else:
            r +=1

    return None  # no solution found


if __name__ == "__main__":
    # Samantha's public parameters
    p = 103687
    q = 1571
    g = 21947
    # public key
    y = 31377


    # find x such that y = g^x mod p

    # find Samantha's private signing key using baby-step giant-step
    x = baby_step_giant_step(g, y, p)

    # Display the result
    print("Samantha's private signing key using baby-step giant-step:", x)
    print("Is y = g^x mod p?", pow(g,x,p) == y)

    d = "510"

    k = 1105

    # Signing using x
    r, s = signing(d, p, q, g, x, k)
    print("Signing using x")
    # Verifying using y
    result = verifying(d, r, s, p, q, g, y)
    print("Verifying using y, result: ", result)
