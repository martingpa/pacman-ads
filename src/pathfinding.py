from collections import deque


def bfs(graph, origin, target):
    if origin == target:
        return origin

    queue = deque([origin])
    parent = {origin: None}

    while queue:
        current = queue.popleft()
        if current == target:
            break
        for node in graph[current]:
            if node not in parent:
                parent[node] = current
                queue.append(node)

    if target not in parent:
        return origin

    step = target
    while parent[step] != origin:
        step = parent[step]

    return step
