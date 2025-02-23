def miller_rabin_test(n, iterations=3):
    def decompose(n_minus_1):
        s = 0
        d = n_minus_1
        while d % 2 == 0:
            d //= 2
            s += 1
        return s, d

    def power_mod(base, exponent, modulus):
        result = 1
        base = base % modulus
        while exponent > 0:
            if (exponent % 2) == 1:
                result = (result * base) % modulus
            exponent = exponent >> 1
            base = (base * base) % modulus
        return result

    print(f"Use the Miller-Rabin test to decide whether the number n={n} is prime or not.")
    print("Check for 3 different bases only if necessary.")
    print(
        "\nImportant note: All answer boxes should be filled in using the convention that those not applicable must be filled in with x.")
    print("All numbers must be filled in as positive numbers mod n.\n")
    print("Solution.\n")

    # Step 1: Decompose (n-1) as 2^s * d
    n_minus_1 = n - 1
    s, d = decompose(n_minus_1)
    print("Decomposition:")
    print(f"s= {s}")
    print(f"t= {d}")
    print(f"t in binary= {bin(d)[2:]}\n")

    bases = [2, 3, 5]
    is_prime = True

    for k, a in enumerate(bases, start=1):
        print(f"Iteration k={k} for a={a} (results mod n):")

        if a == 2:
            for i in range(10):
                power = pow(2, pow(2, i))
                result = power % n
                print(f"2^(2^{i}) = {result}")

        # Step 2: Calculate a^d % n
        x = power_mod(a, d, n)
        print(f"{a}^t = {x}")

        # Show each power up to 2^4 * t
        for r in range(1, s + 1):
            x = power_mod(x, 2, n)
            print(f"{a}^(2^{r} * t) = {x}")

            if x == n - 1:
                print("n may still be prime, found x = n - 1.")
                break
        else:
            print(f"n fails for base {a}, thus composite.")
            is_prime = False
            break
        print(f"n passes the test for base {a}.\n")

    # Conclusion
    print("\nConclusion:")
    print(f"n is prime (yes/no) = {'yes' if is_prime else 'no'}")


# Test the function with n = 6673
miller_rabin_test(6673)