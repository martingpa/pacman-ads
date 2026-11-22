import heapq


# Queue built on a linked list (session 13): enqueue and dequeue are both O(1)
class Node():
    def __init__(self, value):
        self.value = value
        self.next = None

class QueueLinkedList():
    def __init__(self):
        self.head = self.tail = None

    def enqueue(self, value):
        new_node = Node(value)
        if self.tail is not None:
            self.tail.next = new_node
        if self.head is None:
            self.head = new_node
        self.tail = new_node
        return True

    def dequeue(self):
        if self.empty():
            return False
        value = self.head.value
        self.head = self.head.next
        return value

    def empty(self):
        return self.head is None

    def full(self):
        # A linkedlist is never full
        return False


def bfs(graph, origin, target):
    if origin == target:
        return origin

    # create a queue with the origin
    queue = QueueLinkedList()
    queue.enqueue(origin)
    # create the parent dictionary (it is also the visited set)
    parent = {origin: None}

    # while the queue has items
    while not queue.empty():
        # dequeue
        current = queue.dequeue()
        # check vs target
        if current == target:
            break
        # enqueue children we haven't visited
        for node in graph[current]:
            if node not in parent:
                parent[node] = current  #mapping a traversed node from where it was reached
                queue.enqueue(node)

    # target not reachable: stay where we are
    if target not in parent:
        return origin

    # walk back from the target until the parent is the origin
    step = target
    while parent[step] != origin:
        step = parent[step]

    return step        #Next position to move to

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
