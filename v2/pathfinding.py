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

def bfs_distance(graph, origin, target):
    if origin == target:
        return 0
    
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
        return 99
    
    steps = [target]
    while parent[steps[-1]] != origin:
        steps.append(parent[steps[-1]])
    
    return len(steps)        
