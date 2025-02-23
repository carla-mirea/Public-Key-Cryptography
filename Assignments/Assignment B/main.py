import math


# Define the polynomial f(x) = x^2 + 1 mod n
def f(x, n):
    return (x ** 2 + 1) % n


# Function implementing Pollard's ρ algorithm
def pollard_rho(n):
    if n == 1:
        return n  # Trivial case, no prime divisor
    if n % 2 == 0:
        return 2  # Even number, 2 is a divisor

    # Initialize variables
    x0 = 2  # Starting value
    iterations = [x0]
    xj = f(x0, n)  # First value in the sequence
    x2j = f(xj, n)  # Second value in the sequence
    iteration = 1  # Iteration counter
    iterations.append(xj)
    iterations.append(x2j)

    print("Iterations (results mod n):\n")

    while True:
        # Compute GCD
        diff = abs(x2j - iterations[iteration])
        d = math.gcd(diff, n)

        # Print intermediate results
        print(f"x{2 * iteration - 1} = {xj}")
        print(f"x{2 * iteration} = {x2j}")
        print(f"(|x{2 * iteration} − x{iteration}|, n) = ({diff}, {n})  = {d}\n")

        # Check for a non-trivial factor
        if 1 < d < n:
            return d

        # Update the sequence
        xj = f(x2j, n)  # Next xj
        x2j = f(f(x2j, n), n)  # Next x2j (f(f(x)))
        iterations.append(xj)
        iterations.append(x2j)
        iteration += 1

# This method verifies if a number is a perfect square
def is_perfect_square(n):
    # Negative numbers cannot be perfect squares
    if n < 0:
        return False

    root = math.isqrt(n)
    # Check if we obtain the original number
    return root * root == n


# The algorithm tries to express kn as a difference of squares t^2 - s^2,
# looking for values where t^2 - n is a perfect square
def fermat_algorithm(n, B):
    while True:
        if n % 2 == 0:
            return 2, n//2

        # Starting point of t
        t0 = math.isqrt(n)
        print(f"t0 = {t0}")

        # We go from t0 + 1 up to t0 + B
        for i in range(1, B + 1):
            # Calculate the current value of t
            t = t0 + i

            # We check if t^2 - n is a perfect square
            difference = t * t - n
            print(f"t^2 - n = {difference}")
            if is_perfect_square(difference):
                print("yes")
                s = math.isqrt(difference)
                print(f"s = {s} t = {t}")

                # Calculate the factors of n using t and s
                factor1 = (t - s)
                factor2 = (t + s)

                if factor1 != 1 and factor1 != n:
                    return factor1, factor2


if __name__ == "__main__":
    n = 7361
    # result = pollard_rho(n)
    # print(f"One of the divisors for {n} is {result} and {n // result}")

    N = 9291
    factors = fermat_algorithm(N, 10000)
    print("Factors of", N, "are:", factors)

