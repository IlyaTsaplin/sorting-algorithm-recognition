import random
import sys

from matplotlib import pyplot as plt

import sorting_algorithms.default_sort as default_sort
import sorting_algorithms.insertion_sort as insertion_sort
import sorting_algorithms.merge_sort as merge_sort
import sorting_algorithms.quicksort as quicksort
import sorting_algorithms.timsort as timsort
from classes.performance_analysis import PerformanceAnalyser


def plot_comparisons():
    N_LIMIT = 1000
    sys.setrecursionlimit(1500)
    fig, axs = plt.subplots(3, 2)
    row = 0
    col = 0
    for sorting_algorithm in [quicksort.sort, merge_sort.sort, insertion_sort.sort, timsort.sort, default_sort.sort]:
        results_for_sorted = []
        results_for_reversed = []
        results_for_shuffled = []
        for i in range(N_LIMIT):
            data = [x for x in range(i)]
            results_for_sorted.append(PerformanceAnalyser.count_comparisons(sorting_algorithm, data))
            data.reverse()
            results_for_reversed.append(PerformanceAnalyser.count_comparisons(sorting_algorithm, data))
            random.shuffle(data)
            results_for_shuffled.append(PerformanceAnalyser.count_comparisons(sorting_algorithm, data))
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
