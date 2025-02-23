import time

# Function to calculate GCD using the Euclidean algorithm (iterative method)
def gcd_euclidean(a, b):
    # If one of the numbers is 0, return the other number as GCD
    if a == 0:
        return a
    if b == 0:
        return b
    # Continue subtracting the smaller number from the larger until they are equal
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    # Once a == b, the GCD is found
    return a

# Function to check if 'a' is divisible by 'x'
def isDivisible(a, x):
    # Keep subtracting x from a until a becomes smaller than x
    while a >= x:
        a -= x
    # Return True if a is 0, meaning it's divisible, otherwise False
    return a == 0

# Basic GCD algorithm that checks divisibility for each number starting from the minimum of a and b
def gcd_basic(a, b):
    # Start with the smaller of the two numbers
    gcd = min(a, b)
    while not isDivisible(a, gcd) or not isDivisible(b, gcd):
        gcd -= 1
    return gcd

# Function to calculate GCD using the Euclidean algorithm (recursive method)
def gcd_recursive_euclidean(a, b):
    # If a is 0, return b as the GCD
    if a == 0:
        return b

    return gcd_recursive_euclidean(b % a, a)

if __name__ == '__main__':
    tests = [
        (45, 80),
        (121, 17),
        (35, 7),
        (625, 225),
        (245, 45),
        (100, 89),
        (98765432, 12345678),
        (101, 12),
        (24 ** 2, 8 ** 4)
    ]

    for test in tests:
        test_0 = test[0]
        test_1 = test[1]
        print("Current test:", test_0, test_1, "\n")

        print("Recursive Euclidean")
        start = time.time()
        gcd = gcd_recursive_euclidean(test_0, test_1)
        end = time.time()
        print("Time:", end - start, "seconds")
        print("GCD is", gcd, "\n")

        print("Basic Algorithm")
        start = time.time()
        gcd = gcd_basic(test_0, test_1)
        end = time.time()
        print("Time:", end - start, "seconds")
        print("GCD is", gcd, "\n")

        print("Euclidean")
        start = time.time()
        gcd = gcd_euclidean(test_0, test_1)
        end = time.time()
        print("Time:", end - start, "seconds")
        print("GCD is", gcd, "\n")

        print("\n")
