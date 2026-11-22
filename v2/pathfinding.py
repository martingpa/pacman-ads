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

# Depth-first search (graphs session), recursive
def dfs(graph, start, target, visited):
    if start == target:
        return True

    visited.add(start)
    children = graph[start]
    for c in children:
        if c not in visited:
            if dfs(graph, c, target, visited) == True:
                return True
    return False


# Min heap (session 20): the priority queue for Dijkstra
class MinHeap():
    def __init__(self, size):
        self.size = size
        self.next_empty_slot = 0
        self.data = [0] * size

    def push(self, priority):
        # insert priority at next empty position
        if self.next_empty_slot == self.size:
            print("Heap is full!")
            return
        self.data[self.next_empty_slot] = priority
        self._bubble_up(self.next_empty_slot)
        self.next_empty_slot += 1

    def _swap(self, indexa, indexb):
        temp = self.data[indexa]
        self.data[indexa] = self.data[indexb]
        self.data[indexb] = temp

    def _bubble_up(self, index):
        while True:
            if index == 0:
                # we're at root
                break
            parent_index = (index + 1) // 2 -1
            parents_value = self.data[parent_index]
            mispaced_value = self.data[index]
            if mispaced_value < parents_value:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break

    def pop(self) -> int:
        # get the root
        if self.next_empty_slot == 0:
            print("Empty heap!")
            return None
        value = self.data[0]
        # replace it with the last
        self.data[0] = self.data[self.next_empty_slot-1]
        self.next_empty_slot -= 1
        # bubble down
        self._bubble_down(0)
        return value

    def _bubble_down(self, index):
        while True:
            if index >= self.next_empty_slot:
                break
            left_child_index = 2 * (index + 1) -1
            right_child_index = left_child_index + 1
            if left_child_index >= self.next_empty_slot:
                # No children
                break
            elif right_child_index >= self.next_empty_slot:
                # only left child exists
                candidate_index = left_child_index
            elif self.data[left_child_index] < self.data[right_child_index]:
                # Both children exist, and left has lower number, hence higher priority
                candidate_index = left_child_index
            else:
                candidate_index = right_child_index

            if self.data[index] > self.data[candidate_index]:
                self._swap(candidate_index, index)
                index = candidate_index
            else:
                break


def dijkstra(graph, start, target):
    if start == target:
        return start

    # create a priority queue (our MinHeap: a cell is only pushed when its distance improves,
    # at most once per neighbor, and each cell has at most 4 neighbors)
    heap = MinHeap(4 * len(graph) + 1)
    # initialize the distances dictionary
    distances = {}
    # create the parent dictionary (where we came from, like in bfs)
    parent = {start: None}
    # initialize both with start
    heap.push((0, start))
    distances[start] = 0
    # while there are more nodes in priority queue
    while heap.next_empty_slot > 0:
        # pop from priority queue
        d, node = heap.pop()
        # for each children:
        children = graph[node]
        for child, child_distance in children:
            # distance to children = distance to parent + relative distance
            total_child_dist = d + child_distance
            # if distance unknown or better
            if child not in distances or total_child_dist < distances[child]:
                # update the distance
                distances[child] = total_child_dist
                # remember where we came from
                parent[child] = node
                # push to the heap
                heap.push((total_child_dist, child))

    # target not reachable: stay where we are
    if target not in parent:
        return start

    # walk back from the target until the parent is the start
    step = target
    while parent[step] != start:
        step = parent[step]

    return step        #Next position to move to
