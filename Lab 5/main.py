import random
from hashlib import sha256


# Helper Functions
def mod_exp(base, exp, mod):
    """
    Perform modular exponentiation: (base^exp) % mod
    """
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result


def mod_inv(a, p):
    """
    Compute the modular inverse of a under modulo p using the extended Euclidean algorithm.
    """
    return pow(a, -1, p)


def hash_function(*values):
    """
    Hash function to combine input values into a single hash.
    """
    combined = ''.join(map(str, values))
    return int(sha256(combined.encode()).hexdigest(), 16)


class CramerShoup:
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.char_to_int = {char: i for i, char in enumerate(alphabet)}
        self.int_to_char = {i: char for i, char in enumerate(alphabet)}

    def generate_keys(self, p):
        """
        Generate public and private keys.
        p: A large prime number defining the group.
        """
        g1 = random.randint(2, p - 1)
        g2 = random.randint(2, p - 1)

        x1, x2, y1, y2, z = [random.randint(1, p - 2) for _ in range(5)]
        c = (mod_exp(g1, x1, p) * mod_exp(g2, x2, p)) % p
        d = (mod_exp(g1, y1, p) * mod_exp(g2, y2, p)) % p

        h = mod_exp(g1, z, p)

        public_key = (p, g1, g2, c, d, h)
        private_key = (x1, x2, y1, y2, z)

        return public_key, private_key

    def encrypt(self, public_key, plaintext):
        """
        Encrypt plaintext using the public key.
        """
        p, g1, g2, c, d, h = public_key

        # Validate plaintext
        for char in plaintext:
            if char not in self.alphabet:
                raise ValueError(f"Invalid character in plaintext: {char}")

        m = [self.char_to_int[char] for char in plaintext]

        r = random.randint(1, p - 2)
        u1 = mod_exp(g1, r, p)
        u2 = mod_exp(g2, r, p)
        e = [(mod_exp(h, r, p) * mi) % p for mi in m]
        alpha = hash_function(u1, u2, *e) % p
        v = (mod_exp(c, r, p) * mod_exp(d, r * alpha, p)) % p

        ciphertext = (u1, u2, e, v)
        return ciphertext

    def decrypt(self, private_key, public_key, ciphertext):
        """
        Decrypt ciphertext using the private key.
        """
        x1, x2, y1, y2, z = private_key
        p, g1, g2, c, d, h = public_key

        u1, u2, e, v = ciphertext

        # Compute alpha using the same hash function
        alpha = hash_function(u1, u2, *e) % p

        # Validate ciphertext
        v_check = (
                          (mod_exp(u1, x1, p) * mod_exp(u2, x2, p) % p) *
                          (mod_exp(u1, y1, p) * mod_exp(u2, y2, p) % p) ** alpha
                  ) % p

        if v != v_check:
            raise ValueError("Ciphertext validation failed.")

        # Decrypt
        decrypted = [
            (ei * mod_inv(mod_exp(u1, z, p), p)) % p for ei in e
        ]
        plaintext = ''.join(self.int_to_char[mi % len(self.alphabet)] for mi in decrypted)

        return plaintext


# Example Usage
if __name__ == "__main__":
    alphabet = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cramer_shoup = CramerShoup(alphabet)

    # Generate keys
    prime_p = 1013  # Use larger prime for actual security
    public_key, private_key = cramer_shoup.generate_keys(prime_p)

    print("Public Key:", public_key)
    print("Private Key:", private_key)

    # Encrypt
    plaintext = "HELLO_WORLD"
    ciphertext = cramer_shoup.encrypt(public_key, plaintext)
    print("Ciphertext:", ciphertext)

    # Decrypt
    decrypted_text = cramer_shoup.decrypt(private_key, public_key, ciphertext)
    print("Decrypted Text:", decrypted_text)
