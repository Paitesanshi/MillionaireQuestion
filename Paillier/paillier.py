import gmpy2 as gy
import random
import time
import libnum
import paillier.keygen as keygen
import paillier.crypto as crypto

class Paillier(object):
    def __init__(self, pubKey=None, priKey=None):
        self.pubKey = pubKey
        self.priKey = priKey

    def __gen_prime__(self, rs):
        p = gy.mpz_urandomb(rs, 1024)
        while not gy.is_prime(p):
            p += 1
        return p
    
    def __L__(self, x, n):
        res = gy.div((x - 1), n)
        # this step is essential, directly using "/" causes bugs
        # due to the floating representation in python
        return res
    def __get_random__(self,x):
        return random.getrandbits(x)
    def __key_gen__(self):
        # generate random state
        while True:
            rs = gy.random_state(int(time.time()))
            p = self.__gen_prime__(rs)
            q = self.__gen_prime__(rs)
            n = p * q
            lmd =(p - 1) * (q - 1)
            # originally, lmd(lambda) is the least common multiple. 
            # However, if using p,q of equivalent length, then lmd = (p-1)*(q-1)
            if gy.gcd(n, lmd) == 1:
                # This property is assured if both primes are of equal length
                break
        g = n + 1
        mu = gy.invert(lmd, n)
        #Originally,
        # g would be a random number smaller than n^2, 
        # and mu = (L(g^lambda mod n^2))^(-1) mod n
        # Since q, p are of equivalent length, step can be simplified.
        self.pubKey = [n, g]
        self.priKey = [lmd, mu]
        return self.pubKey,self.priKey
        
    def decipher(self,pubKey,priKey, ciphertext):
        n, g = pubKey
        lmd, mu = priKey
        m =  self.__L__(gy.powmod(ciphertext, lmd, n ** 2), n) * mu % n
        print("raw message:", m)
        plaintext = libnum.n2s(int(m))
        return plaintext

    def encipher(self, pubkey,plaintext):
        m = libnum.s2n(plaintext)
        n, g = pubkey
        r = gy.mpz_random(gy.random_state(int(time.time())), n**2)
        while gy.gcd(n, r)  != 1:
            r += 1
        ciphertext = gy.powmod(g, m, n ** 2) * gy.powmod(r, n, n ** 2) % (n ** 2)
        return ciphertext

# if __name__ == "__main__":
#     pai = Paillier()
#     pai.__key_gen__()
#     pubKey = pai.pubKey
#     print("Public/Private key generated.")
#     plaintext = input("Enter your text: ")
#     # plaintext = 'Cat is the cutest.'
#     print("Original text:", plaintext)
#     ciphertext = pai.encipher(plaintext)
#     print("Ciphertext:", ciphertext)
#     deciphertext = pai.decipher(ciphertext)
#     print("Deciphertext: ", deciphertext)
