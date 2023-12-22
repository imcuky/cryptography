import hashlib
import hmac

# HMACK(M) = H[(K+ ⊕ opad) || H[(K+ ⊕ ipad) || M] ] 
def hmac_sha512(key, message):

    block_size = 128  # each block contains 4 bits total of 512 bits

    # padded with zeros so that the result is equal to the block length of the hash code
    if len(key) < block_size:
        # to byte string
        key = key + b'\x00' * (block_size - len(key)) 

    # (K+ ⊕ ipad) use '^' bitwise operation
    o_key_pad = bytes([ x ^ 0x5C for x in key])
    # (K+ ⊕ opad)
    i_key_pad = bytes([ x ^ 0x36 for x in key])

    # apply SHA-512
    inner_hash = hashlib.sha512(i_key_pad + message).digest()
    outer_hash = hashlib.sha512(o_key_pad + inner_hash).hexdigest()

    return outer_hash

if __name__ == "__main__":

    
    input_string = "This input string is being used to test my own implementation of HMAC-SHA-512."
    key = b"123456789"

    # Implementing HMAC-SHA-512
    imp_hmac = hmac_sha512(key, input_string.encode())

    # Using library to calculate HMAC-SHA-512 for verification
    library_hmac = hmac.new(key, input_string.encode(), hashlib.sha512).hexdigest()

    # Displaying results
    print("HMAC-SHA-512 implementation:", imp_hmac)
    print("Library HMAC-SHA-512 implementation:", library_hmac)
    print("Confirm Implementation: ", imp_hmac == library_hmac)
