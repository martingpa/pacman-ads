import heapq
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
                parent[node] = current  #mapping a traversed node from where it was reached
                queue.append(node)
    
    if target not in parent:
        return origin
    
    steps = [target]
    while parent[steps[-1]] != origin:
        steps.append(parent[steps[-1]])
    
    return steps[-1]        #Next position to move to

def dijkstra(graph, start):
    # create a priority queue
    heap = []
    # initialize the distances dictionary
    distances = {}
    # initialize both with start
    heapq.heappush(heap, (0, start))
    distances[start] = 0
    # while there are more nodes in priority queue
    while len(heap) > 0:
        # pop from priority queue
        d, node = heapq.heappop(heap)
        # for each children:
        children = graph[node]
        for child, child_distance in children:
            # distance to children = distance to parent + relative distance
            total_child_dist = d + child_distance
            # if distance unknown or better
            if child not in distances or total_child_dist < distances[child]:
                # update the distance
                distances[child] = total_child_dist
                # push to the heap
                heapq.heappush(heap, (total_child_dist, child))
    # return distances
    return distances
