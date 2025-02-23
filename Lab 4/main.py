import random


class RabinCryptosystem:
    def __init__(self):
        self.alphabet = '_abcdefghijklmnopqrstuvwxyz'  # _ is space
        self.char_to_num = {char: idx for idx, char in enumerate(self.alphabet)}
        self.num_to_char = {idx: char for idx, char in enumerate(self.alphabet)}
        self.result = ""

    def is_prime(self, num):
        """Check if a number is prime."""
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def generate_prime(self):
        """Generate a prime number p such that p % 4 == 3."""
        while True:
            p = random.randint(1000, 5000)
            if self.is_prime(p) and p % 4 == 3:
                return p

    def extended_gcd(self, a, b):
        """Extended Euclidean Algorithm to compute modular inverses."""
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = self.extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    def generate_keys(self):
        """Generate public and private keys."""
        p = self.generate_prime()
        q = self.generate_prime()
        n = p * q
        self.public_key = n
        self.private_key = (p, q)
        return self.public_key, self.private_key

    def validate_plaintext(self, plaintext):
        return all(char in self.alphabet for char in plaintext)

    def validate_ciphertext(self, ciphertext):
        """Validate that ciphertext values are within the valid range."""
        if not all(0 <= c < self.public_key for c in ciphertext):
            raise ValueError("Invalid ciphertext: values must be in range [0, n).")

    def plaintext_to_numbers(self, plaintext):
        return [self.char_to_num[char] for char in plaintext]

    def numbers_to_plaintext(self, numbers):
        return ''.join(self.num_to_char[num] for num in numbers)

    def split_into_blocks(self, data, block_size):
        return [data[i:i + block_size] for i in range(0, len(data), block_size)]

    def encrypt(self, plaintext, k):
        """Encrypt plaintext using the public key."""
        if not self.validate_plaintext(plaintext):
            raise ValueError("Invalid plaintext: contains unsupported characters.")

        blocks = self.split_into_blocks(plaintext, k)

        if len(blocks[-1]) < k:
            blocks[-1] = blocks[-1] + '_' * (k - len(blocks[-1]))

        ciphertext = []

        for block in blocks:
            block_numbers = self.plaintext_to_numbers(block)
            num = sum(x * (len(self.alphabet) ** i) for i, x in enumerate(block_numbers))  # convert into a number

            # Apply the Rabin encryption formula: c = (num^2) mod n
            c = (num * num) % self.public_key
            ciphertext.append(c)

        return ciphertext

    def num_to_letters_de(self, num):
        """Convert number to letters in blocks for plaintext."""
        letters = ""
        while num > 0:
            num, remainder = divmod(num, 27)
            if remainder == 0:
                letters = letters + "_"
            else:
                letters = letters + chr(96 + remainder)
        return letters

    def decrypt(self, ciphertext):
        """Decrypt ciphertext using private key."""
        self.validate_ciphertext(ciphertext)

        p, q = self.private_key
        n = p * q
        decrypted_text = []

        for c in ciphertext:
            m_p = pow(c, (p + 1) // 4, p)
            m_q = pow(c, (q + 1) // 4, q)
            _, yp, yq = self.extended_gcd(p, q)

            r1 = (yp * p * m_q + yq * q * m_p) % n
            r2 = n - r1
            r3 = (yp * p * m_q - yq * q * m_p) % n
            r4 = n - r3

            roots = [r1, r2, r3, r4]

            valid_root = next((root for root in roots if root < (27 ** k)), None)
            if valid_root is None:
                raise ValueError("Decryption failed: no valid roots found.")

            decrypted_block = self.num_to_letters_de(valid_root)
            decrypted_text.append(decrypted_block)

        return ''.join(decrypted_text)


if __name__ == "__main__":

    try:
        rabin = RabinCryptosystem()

        print("Generating keys...")
        public_key, private_key = rabin.generate_keys()
        print(f"Public Key (n): {public_key}")
        print(f"Private Key (p, q): {private_key}")

        # Encryption
        plaintext = "an_example"
        print(f"\nPlaintext: {plaintext}")
        k = 2  # Block size for plaintext
        ciphertext = rabin.encrypt(plaintext, k)
        print(f"Ciphertext: {ciphertext}")

        # Decryption
        print("\nDecrypting...")
        l = 3  # Block size for ciphertext
        decrypted_text = rabin.decrypt(ciphertext)
        print(f"Decrypted Text: {decrypted_text}")

    except ValueError as e:
        print(f"Error:{e}")
