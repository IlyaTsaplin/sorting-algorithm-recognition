import random

import matplotlib.pyplot as plt


def nearly_sorted(sorted_array, number_of_swaps=None):
    """
    Create nearly sorted array from sorted array
    Performs random swaps between neighbours
    @param sorted_array: Sorted array
    @param number_of_swaps: Number of random swaps performed. Equals length of sorted array if not provided
    @return: Nearly sorted array
    """

    if number_of_swaps is None:
        number_of_swaps = len(sorted_array)

    copy = sorted_array.copy()
    for i in range(number_of_swaps):
        index = random.randint(0, len(copy) - 2)
        copy[index], copy[index + 1] = copy[index + 1], copy[index]

    return copy


if __name__ == '__main__':
    arr = [x for x in range(100)]
    nearly_sorted = nearly_sorted(arr, len(arr))
    print(arr)
    print(nearly_sorted)
    plt.bar(range(len(arr)), arr, label='sorted')
    plt.bar(range(len(arr)), nearly_sorted, label='nearly_sorted')
    plt.legend()
    plt.show()
