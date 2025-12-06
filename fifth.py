import sys
import heapq

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    h = int(next(it))
    w = int(next(it))
    n = int(next(it))
    grid = [list(next(it)) for _ in range(h)]

    V = h * w
    weight = [0] * V
    terminal_positions = []
    terminal_ids = {}

    for i in range(h):
        for j in range(w):
            idx = i * w + j
            ch = grid[i][j]
            if ch == 'o':
                weight[idx] = 9
                terminal_ids[idx] = len(terminal_positions)
                terminal_positions.append(idx)
            elif ch == '*':
                weight[idx] = 9
                terminal_ids[idx] = len(terminal_positions)
                terminal_positions.append(idx)
            else:
                weight[idx] = int(ch)

    K = len(terminal_positions)

    def neighbors(idx):
        i = idx // w
        j = idx % w
        res = []
        if i > 0:
            res.append((i - 1) * w + j)
        if i < h - 1:
            res.append((i + 1) * w + j)
        if j > 0:
            res.append(i * w + (j - 1))
        if j < w - 1:
            res.append(i * w + (j + 1))
        return res

    adj = [neighbors(idx) for idx in range(V)]

    INF = 10 ** 9
    dp = [[INF] * V for _ in range(1 << K)]
    prev_type = [[-1] * V for _ in range(1 << K)]
    prev_data = [[-1] * V for _ in range(1 << K)]

    for t, idx in enumerate(terminal_positions):
        dp[1 << t][idx] = weight[idx]
        prev_type[1 << t][idx] = 0

    for mask in range(1, 1 << K):
        if mask & (mask - 1):
            lsb = mask & -mask
            submask = mask
            while submask:
                if submask & lsb and submask != mask and submask != 0:
                    other = mask ^ submask
                    for v in range(V):
                        if dp[submask][v] < INF and dp[other][v] < INF:
                            new_cost = dp[submask][v] + dp[other][v] - weight[v]
                            if new_cost < dp[mask][v]:
                                dp[mask][v] = new_cost
                                prev_type[mask][v] = 1
                                prev_data[mask][v] = submask
                submask = (submask - 1) & mask

        pq = []
        for v in range(V):
            if dp[mask][v] < INF:
                heapq.heappush(pq, (dp[mask][v], v))
        while pq:
            d, v = heapq.heappop(pq)
            if d != dp[mask][v]:
                continue
            for u in adj[v]:
                nd = d + weight[u]
                if nd < dp[mask][u]:
                    dp[mask][u] = nd
                    prev_type[mask][u] = 2
                    prev_data[mask][u] = v
                    heapq.heappush(pq, (nd, u))

    full_mask = (1 << K) - 1
    best_cost = min(dp[full_mask])
    best_v = min(range(V), key=lambda v: dp[full_mask][v])

    def get_vertices(mask, v):
        if prev_type[mask][v] == -1:
            return set()
        if prev_type[mask][v] == 0:
            return {v}
        if prev_type[mask][v] == 1:
            submask = prev_data[mask][v]
            s1 = get_vertices(submask, v)
            s2 = get_vertices(mask ^ submask, v)
            return s1 | s2
        if prev_type[mask][v] == 2:
            u = prev_data[mask][v]
            s = get_vertices(mask, u)
            s.add(v)
            return s

    dug = get_vertices(full_mask, best_v)

    print(best_cost)
    for i in range(h):
        row = []
        for j in range(w):
            idx = i * w + j
            ch = grid[i][j]
            if ch not in ('*', 'o') and idx in dug:
                row.append('.')
            else:
                row.append(ch)
        print(''.join(row))

if __name__ == "__main__":
    solve()