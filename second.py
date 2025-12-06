import sys
import math

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))

    d = arr[0]
    for x in arr[1:]:
        d = math.gcd(d, x)

    M = max(arr)
    total = M // d
    moves = total - n

    print("Serge" if moves % 2 == 1 else "Alex")

if __name__ == "__main__":
    main()