import heapq
import os

# the high-score table is saved next to this file, one score per line
SCORES_FILE = os.path.join(os.path.dirname(__file__), "scores.txt")


# Top k with a heap (session 20)
def topk(arr, k):
    top = []
    # iterate the array
    for element in arr:
        # push the element
        heapq.heappush(top, element)
        # if size is larger then pop
        if len(top) > k:
            heapq.heappop(top)
    return top


# Mergesort (session 11)
def merge(arr1, arr2):
    # we create an empty solution array
    solution = []
    # we setup two pointers, each one pointing to the first element of the input arrays

    p1 = 0
    p2 = 0
    while p1 < len(arr1) and p2 < len(arr2):
        # we compare the values under the pointers
        if arr1[p1] < arr2[p2]:
            # if the value below first pointer is smaller I throw that value to the solution
            solution.append(arr1[p1])
            p1 += 1
            # if not then we use the value from the second array
        else:
            solution.append(arr2[p2])
            p2 += 1
        # then move the pointer that had the smallest value
        # do this while both pointers are smaller than len of its array

    # at this point, either of the two is exhausted
    while p1 < len(arr1):
        solution.append(arr1[p1])
        p1 += 1

    while p2 < len(arr2):
        solution.append(arr2[p2])
        p2 += 1
    # now take the array whose pointer still not pointing to the last and append all its remaining elements to the solution array

    return solution


def msort(arr):
    if len(arr) < 2:
        return arr
    # divide it in half
    mid = len(arr) // 2
    left_half = []
    right_half = []
    for i in range(len(arr)):
        if i < mid:
            left_half.append(arr[i])
        else:
            right_half.append(arr[i])
    # recurse until len(arr) is 1
    left_half_sorted = msort(left_half)
    right_half_sorted = msort(right_half)
    # combine both sorted halves using merge
    return merge(left_half_sorted, right_half_sorted)


# Binary search (session 8)
def bsearch(data, target):
    # set max and min indices
    max = len(data)-1
    min = 0
    # do it while min is smaller than max
    while min <= max:
        # find the mid element and compare to target
        mid = min + (max-min)//2
        # if target is less than middle then move the max to mid -1
        if target < data[mid]:
            max = mid -1
        elif target > data[mid]:
            # if target is larger than middle then move min to mid +1
            min = mid+1
        else:
            # if target is mid then return it
            return mid


def save_score(score):
    # read the old scores (there is no file before the first game)
    scores = []
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE) as file:
            for line in file:
                if line.strip() != "":
                    scores.append(int(line))
    scores.append(score)

    # keep only the best 5 (heap), then put them in order (mergesort, lowest first)
    top = msort(topk(scores, 5))

    # write the table back, one score per line
    with open(SCORES_FILE, "w") as file:
        for s in top:
            file.write(f"{s}\n")

    # find our place with binary search (works because the list is sorted)
    index = bsearch(top, score)
    if index is None:
        rank = None                     # not in the top 5
    else:
        rank = len(top) - index         # the highest score is last, so it's #1
    best = top[-1]
    return rank, best
