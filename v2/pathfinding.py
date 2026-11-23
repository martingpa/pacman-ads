from collections import deque


def bfs(graph, origin, target):
    if origin == target:
        return origin

    # create a queue with the origin
    queue = deque([origin])
    # create the parent dictionary (it is also the visited set)
    parent = {origin: None}

    # while the queue has items
    while queue:
        # dequeue
        current = queue.popleft()
        # check vs target
        if current == target:
            break
        # enqueue children we haven't visited
        for node in graph[current]:
            if node not in parent:
                parent[node] = current  #mapping a traversed node from where it was reached
                queue.append(node)

    # target not reachable: stay where we are
    if target not in parent:
        return origin

    # walk back from the target until the parent is the origin
    step = target
    while parent[step] != origin:
        step = parent[step]

    return step        #Next position to move to
