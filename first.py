import sys
import math

def main():
    n = int(sys.stdin.readline().strip())
    temp = n
    d = 1
    unique_primes = 0
    limit = int(math.isqrt(n)) + 1

    p = 2
    while p <= limit and p * p <= temp:
        if temp % p == 0:
            cnt = 0
            unique_primes += 1
            while temp % p == 0:
                temp //= p
                cnt += 1
            d *= (cnt + 1)
        p += 1 if p == 2 else 2

    if temp > 1:
        d *= 2
        unique_primes += 1

    print(d - 1 - unique_primes)

if __name__ == "__main__":
    main()