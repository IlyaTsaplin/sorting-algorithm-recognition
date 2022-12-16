import sys
import random
import pandas as pd
from identification.sorting_identification import count_comparisons, measure_algorithm
from sorting_algorithms.quicksort import quick_sort
from sorting_algorithms.mergesort import merge_sort
from sorting_algorithms.insertionsort import insertion_sort
from sorting_algorithms.timsort import timsort
from matplotlib import pyplot as plt


def plot_comparisons():
    N_LIMIT = 1000
    sys.setrecursionlimit(1500)
    fig, axs = plt.subplots(3, 2)
    row = 0
    col = 0
    for sorting_algorithm in [quick_sort, merge_sort, insertion_sort, timsort, default_sort]:
        results_for_sorted = []
        results_for_reversed = []
        results_for_shuffled = []
        for i in range(N_LIMIT):
            data = [x for x in range(i)]
            results_for_sorted.append(count_comparisons(sorting_algorithm, data))
            data.reverse()
            results_for_reversed.append(count_comparisons(sorting_algorithm, data))
            random.shuffle(data)
            results_for_shuffled.append(count_comparisons(sorting_algorithm, data))
        axs[row, col].plot(range(N_LIMIT), results_for_sorted, label='sorted')
        axs[row, col].plot(range(N_LIMIT), results_for_reversed, label='reversed')
        axs[row, col].plot(range(N_LIMIT), results_for_shuffled, label='shuffled')
        axs[row, col].legend()
        axs[row, col].grid()
        axs[row, col].set_xlabel('Number of elements')
        axs[row, col].set_ylabel('Number of comparisons')
        axs[row, col].set_title(sorting_algorithm.__name__)

        col = (col + 1) % 2
        if col == 0:
            row += 1
    fig.tight_layout()
    plt.show()


def default_sort(data):
    sorted_data = sorted(data)
    for i in range(len(data)):
        data[i] = sorted_data[i]


def main():
    df = measure_algorithm(quick_sort)
    df = pd.concat([df, measure_algorithm(merge_sort)])
    df = pd.concat([df, measure_algorithm(insertion_sort)])
    df = pd.concat([df, measure_algorithm(timsort)])
    df = pd.concat([df, measure_algorithm(default_sort)])

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)

    # plot_comparisons()


if __name__ == '__main__':
    main()
