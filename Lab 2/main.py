# We will solve the congruence system based on
# the Chinese remainder Theorem:
# there always exists an x that satisfies given congruences

# k is the size of n[] and r[]
# Returns the smallest number x such that:
# x % n[0] = r[0],
# x % n[1] = r[1],
# ..................
# x % n[k-2] = r[k-1]
# We assume that the numbers in n[]
# are pairwise coprime (gcd for every pair is 1)


# The brut solution:
def solve_system(n, r, k):
    # Initialize the result
    x = 1

    # This loop will always break -> CRT
    while (True):
        # For all j to k, we check if x is a solution
        j = 0
        while (j < k):
            if (x % n[j] != r[j]):
                break
            j += 1

        # If x matches everywhere, we found the min solution
        # otherwise try another number
        if (j == k):
            return x

        x += 1


# The efficient solution:
# We use CRT to solve the system of congruences,
# reducing the problem to a single congruence modulo the product of the moduli
# We apply Extended Euclidean Algorithm to find the modular inverse of a number
# a modulo m
# modular inverse: for a number a modulo m is a number x such that
# when multiplied by a, gives a remainder of 1 when divided by m
# a and m have to be coprime

# We calculate recursively the gcd and the x and y coefficients that satisfy:
# gcd(a,b) = a * x + b * y
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


# We use gcd, x and y from the extended_gcd() for gcd = 1 to find the modular inverse:
# a * x + m * y = 1 => a * x ≡ 1 (mod m)
def modular_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("The numbers are not coprime. There is no inverse!")
    else:
        return x % m


# We calculate the minimum solution of the system
def chinese_remainder_theorem(n, r):
    # The product of all moduli
    product = 1
    for i in n:
        product *= i

    # Initialize the result
    x = 0

    # Compute the result using the formula
    for i, j in zip(r, n):
        prod = product // j # Product except the current n
        inverse = modular_inverse(prod, j)
        x += i * prod * inverse

    # Return the result modulo the product of all moduli
    return x % product


# x ≡ 2 (mod 3)
# x ≡ 3 (mod 5)
# x ≡ 2 (mod 7)
r = [2, 3, 1]
n = [3, 4, 5]
k = len(n)

solution_1 = solve_system(n, r, k)
solution_2 = chinese_remainder_theorem(n, r)

print("Raw solution: x is", solution_1)
print("Efficient solution: x is", solution_2)
