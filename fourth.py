#не проходит по последнему тесту

import sys
from collections import deque


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    k = int(next(it))
    bases = []
    base_coords = set()
    for _ in range(k):
        r = int(next(it))
        c = int(next(it))
        bases.append((r, c))
        base_coords.add((r, c))

    start = (1, 1)
    target = (n, m)
    is_target_base = target in base_coords

    base_index = {}
    for idx, (r, c) in enumerate(bases):
        base_index[(r, c)] = idx
    start_id = base_index[start]
    if is_target_base:
        target_id = base_index[target]
    else:
        target_id = k

    rows = {}
    cols = {}
    for idx, (r, c) in enumerate(bases):
        rows.setdefault(r, []).append(idx)
        cols.setdefault(c, []).append(idx)

    V = k + (0 if is_target_base else 1)
    dist = [10 ** 9] * V
    dist[start_id] = 0

    row_activated = set()
    col_activated = set()

    dq = deque([start_id])

    while dq:
        u = dq.popleft()
        r, c = bases[u] if u < k else target

        if u < k:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in base_index:
                    v = base_index[(nr, nc)]
                    if dist[v] > dist[u]:
                        dist[v] = dist[u]
                        dq.appendleft(v)

            if r not in row_activated:
                row_activated.add(r)
                for v in rows.get(r, []):
                    if dist[v] > dist[u] + 1:
                        dist[v] = dist[u] + 1
                        dq.append(v)

            if c not in col_activated:
                col_activated.add(c)
                for v in cols.get(c, []):
                    if dist[v] > dist[u] + 1:
                        dist[v] = dist[u] + 1
                        dq.append(v)

    if is_target_base:
        ans = dist[target_id]
    else:
        ans = 10 ** 9
        for idx in range(k):
            br, bc = bases[idx]
            if br == n or bc == m:
                ans = min(ans, dist[idx] + 1)
        if n in row_activated or m in col_activated:
            for idx in range(k):
                br, bc = bases[idx]
                if br == n or bc == m:
                    ans = min(ans, dist[idx])

    if ans == 10 ** 9:
        print(-1)
    else:
        print(ans)


if __name__ == "__main__":
    main()