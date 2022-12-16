import random
import copy
import pandas as pd
from classes.element import Element


def count_comparisons(sort_algo, data):
    """
    Measures comparisons performed by sorting algorithm on given data
    :param sort_algo: sorting function
    :param data: data for sorting
    :return: Number of comparisons performed
    """
    data = copy.deepcopy(data)
    Element.reset_counter()
    sort_algo(data)
    return Element.comparison_counter


def check_stability(sorting_algorithm):
    """
    Checks if sorting algorithm is stable
    :param sorting_algorithm:
    :return: Bool value. True if algorithm is stable, False otherwise
    """
    data = []
    for i in range(100):
        data.append(Element(random.randint(0, 100), i))
    sorting_algorithm(data)
    return sequential_are_ascending(data)


def sequential_are_ascending(data):
    """
    Checks if sequential criteria of equal elements next to each other are in ascending order
    :param data: List of Elements
    :return: True if ascending, False otherwise
    """
    for i in range(1, len(data)):
        if data[i].sorting_criteria == data[i - 1].sorting_criteria and \
                data[i].sequential_id < data[i - 1].sequential_id:
            return False
    return True


def measure_algorithm(algorithm, data_size=100, seed=0):
    """
    Measures sorting algorithm characteristics
    :param seed: seed for shuffling data
    :param algorithm: sorting function
    :param data_size: size of data
    :return: Dataframe (comparisons_sorted, comparisons_reversed, comparisons_shuffled, is_stable)
    """
    data = [Element(x, x) for x in range(data_size)]
    comparisons_sorted = count_comparisons(algorithm, data)
    data.reverse()
    comparisons_reversed = count_comparisons(algorithm, data)
    random.seed(seed)
    random.shuffle(data)
    comparisons_shuffled = count_comparisons(algorithm, data)
    is_stable = check_stability(algorithm)

    return pd.DataFrame(
        data={'Comparisons on sorted data': [comparisons_sorted],
              'Comparisons of reversed data': [comparisons_reversed],
              'Comparisons of shuffled data': [comparisons_shuffled],
              'Is stable': [is_stable]})
