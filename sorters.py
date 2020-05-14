import random, math

def swap(array, i, j):
    array[i], array[j] = array[j], array[i]

def reshuffle(array):
    if array:
        n = len(array)
        for i in range(n):
            j = random.randint(0, n-1)
            yield [(i, j, False)]
            swap(array, i, j)
            yield [(i, j, True)]


def bubble_sort(array):
    if not array: return

    for i in range(len(array)-1, -1, -1):
        for j in range(0, i):
            yield [(i, j, False)]
            if (array[i] < array[j]):
                swap(array, i, j)
                yield [(i, j, True)]

def insertion_sort(array):
    if not array: return
    n = len(array)
    for i in range(1, n):
        index = i
        for j in range(i-1, -1, -1):
            yield [(index, j, False)]
            if array[j] < array[index]:
                break
            swap(array, index, j)
            index = j
            yield [(index, j, True)]

def selection_sort(array):
    if not array: return
    n = len(array)
    for i in range(n):
        index = i
        value = array[i]
        for j in range(i + 1, n):
            yield [(index, j, False)]
            if array[j] < value:
                index = j
                value = array[j]
        swap(array, i, index)
        yield [(index, i, True)]

def in_place_quick_sort(array):
    if not array: return
    yield from quick_sort_partition(array, 0, len(array))

def quick_sort_partition(array, start, end):
    if end == start: return
    pivot_index = start
    last_unsorted_index = end - 1
    i = start + 1
    while (i <= last_unsorted_index):
        yield [(pivot_index, i, False)]
        if array[i] <= array[pivot_index]:
            swap(array, pivot_index, i)
            yield [(pivot_index, i, True)]
            pivot_index = i
            i += 1
        else:
            swap(array, i, last_unsorted_index)
            yield [(i, last_unsorted_index, True)]
            last_unsorted_index -= 1
    yield from quick_sort_partition(array, start, pivot_index)
    yield from quick_sort_partition(array, pivot_index + 1, end)

def merge_sort(array):
    if not array: return
    yield from merge_sort_partition(array, 0, len(array))

def merge_sort_partition(array, start, end):
    if start + 1 == end: return
    mid_point = math.ceil((end + start) / 2)
    yield from merge_sort_partition(array, start, mid_point)
    yield from merge_sort_partition(array, mid_point, end)
    result = []
    left_index = start
    right_index = mid_point

    def poll(index):
        result.append(array[index])
        return index + 1

    while left_index != mid_point and right_index != end:
        yield [(left_index, right_index, False)]
        if array[left_index] < array[right_index]:
            left_index = poll(left_index)
        else:
            right_index = poll(right_index)
    while left_index != mid_point:
        yield [(left_index, left_index, False)]
        left_index = poll(left_index)
    while right_index != end:
        yield [(right_index, right_index, False)]
        right_index = poll(right_index)

    #array[start:end] = result
    for i in range(len(result)):
        yield [(start + i, start + i, False)]
        array[start + i] = result[i]

sorting_algorithms = [ merge_sort, in_place_quick_sort, bubble_sort, insertion_sort, selection_sort ]
