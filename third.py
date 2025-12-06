import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    t = int(data[1])
    a = list(map(int, data[2:2 + n]))

    left = 0
    current_sum = 0
    max_len = 0

    for right in range(n):
        current_sum += a[right]
        while current_sum > t and left <= right:
            current_sum -= a[left]
            left += 1
        max_len = max(max_len, right - left + 1)

    print(max_len)

if __name__ == "__main__":
    main()