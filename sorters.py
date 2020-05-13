import random

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

sorting_algorithms = [ bubble_sort, insertion_sort ]
