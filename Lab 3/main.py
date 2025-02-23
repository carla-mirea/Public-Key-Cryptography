import math


# This method verifies if a number is a perfect square
def is_perfect_square(n):
    # Negative numbers cannot be perfect squares
    if n < 0:
        return False

    root = math.isqrt(n)
    # Check if we obtain the original number
    return root * root == n


# The algorithm tries to express kn as a difference of squares t^2 - s^2,
# looking for values where t^2 - kn is a perfect square
def generalized_fermat_algorithm(n, B):
    # We start with the value 1 for k, multiplier for the generalized algorithm
    k = 1

    while True:
        if n % 2 == 0:
            return 2, n//2

        # Calculate k * n
        kn = k * n

        # Starting point of t
        t0 = math.isqrt(kn)

        # We go from t0 + 1 up to t0 + B
        for i in range(1, B + 1):
            # Calculate the current value of t
            t = t0 + i

            # We check if t^2 - kn is a perfect square
            difference = t * t - kn
            if is_perfect_square(difference):
                s = math.isqrt(difference)

                # Calculate the factors of n using t and s
                factor1 = (t - s)
                factor2 = (t + s)

                if factor1 % k == 0 or factor2 % k == 0:
                    if factor1 % k == 0:
                        factor1 = factor1 // k
                    else:
                        factor2 = factor2 // k

                    if factor1 != 1 and factor1 != n:
                        return factor1, factor2

        # Increment k to try with a new multiple of n
        k += 1


if __name__ == "__main__":
    N = 200819
    factors = generalized_fermat_algorithm(N, 10)
    print("Factors of", N, "are:", factors)
