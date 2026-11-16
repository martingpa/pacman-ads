from collections import deque


def bfs_next_step(start, target, neighbors):
    """BFS from start to target; return the first cell of the shortest path.

    neighbors: function that takes a cell and returns its walkable neighbor cells.
    """
    if start == target:
        return start
    queue = deque([start])
    parent = {start: None}          # Also acts as the visited set
    while queue:
        current = queue.popleft()
        if current == target:
            break
        for nxt in neighbors(current):
            if nxt not in parent:
                parent[nxt] = current
                queue.append(nxt)
    if target not in parent:        # Unreachable: stay put
        return start
    step = target                   # Walk back until the cell right after start
    while parent[step] != start:
        step = parent[step]
    return step