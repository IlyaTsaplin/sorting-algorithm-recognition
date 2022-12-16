import copy
import pandas as pd
from classes.element import Element


class ErrorInSorting(Exception):
    """
    Exception for errors in provided sorting algorithm code
    """
    pass


class PerformanceAnalyser:
    """
    Checks sorting algorithm correctness and simultaneously analyses performance
    """
    shuffled_elements = [76, 91, 88, 92, 51, 86, 98, 8, 5, 45, 83, 36, 47, 58, 19, 97, 52, 12, 21, 33, 80, 93, 75, 89,
                         40, 69, 77, 70, 16, 62, 6, 18, 56, 0, 13, 71, 65, 11, 55, 85, 15, 29, 95, 79, 84, 78, 68, 23,
                         42, 32, 26, 49, 30, 74, 1, 53, 3, 99, 27, 64, 41, 7, 96, 4, 43, 9, 73, 59, 44, 10, 24, 28, 39,
                         57, 90, 17, 60, 81, 22, 31, 67, 20, 87, 14, 63, 82, 35, 72, 25, 54, 38, 61, 48, 37, 34, 66, 94,
                         46, 2, 50]
    elements_for_stable_check = [11, 86, 96, 16, 19, 4, 10, 89, 69, 87, 50, 90, 67, 35, 66, 30, 27, 86, 75, 53, 74, 35,
                                 57, 63, 84, 82, 89, 45, 10, 41, 78, 14, 62, 75, 80, 42, 24, 31, 2, 93, 34, 14, 90, 28,
                                 47, 21, 42, 54, 7, 12, 100, 18, 89, 28, 5, 73, 81, 68, 77, 87, 9, 3, 15, 81, 24, 77,
                                 73, 15, 50, 11, 47, 14, 4, 77, 2, 24, 23, 91, 15, 61, 26, 93, 7, 86, 2, 69, 54, 79, 12,
                                 33, 8, 28, 9, 82, 38, 44, 55, 23, 7, 64]

    ordered_data = [Element(x, x) for x in range(100)]
    shuffled_data = [Element(shuffled_element, i) for i, shuffled_element in enumerate(shuffled_elements)]
    stable_check_data = [Element(element, i) for i, element in enumerate(elements_for_stable_check)]

    @classmethod
    def count_comparisons(cls, sorting_algorithm, data):
        """
        Measures comparisons performed by sorting algorithm on given data
        :param sorting_algorithm: sorting function
        :param data: data for sorting
        :return: Number of comparisons performed
        """
        data = copy.deepcopy(data)
        Element.reset_counter()

        try:
            sorting_algorithm(data)
        except Exception as exception:
            raise ErrorInSorting(exception)

        comparison_counter = Element.comparison_counter
        assert (cls.is_sorted(data))
        return comparison_counter

    @staticmethod
    def is_sorted(data):
        return all(data[i] <= data[i + 1] for i in range(len(data) - 1))

    @classmethod
    def check_stability(cls, sorting_algorithm):
        """
        Checks if sorting algorithm is stable
        :param sorting_algorithm:
        :return: Bool value. True if algorithm is stable, False otherwise
        """
        data = cls.stable_check_data.copy()

        try:
            sorting_algorithm(data)
        except Exception as exception:
            raise ErrorInSorting(exception)

        assert (cls.is_sorted(data))
        return PerformanceAnalyser.sequential_are_ascending(data)

    @staticmethod
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

    @classmethod
    def measure_algorithm(cls, algorithm):
        """
        Measures sorting algorithm characteristics
        :param algorithm: sorting function
        :return: Dataframe (comparisons_sorted, comparisons_reversed, comparisons_shuffled, is_stable)
        """
        data = cls.ordered_data.copy()
        comparisons_sorted = PerformanceAnalyser.count_comparisons(algorithm, data)
        data.reverse()
        comparisons_reversed = PerformanceAnalyser.count_comparisons(algorithm, data)
        data = cls.shuffled_data.copy()
        comparisons_shuffled = PerformanceAnalyser.count_comparisons(algorithm, data)
        is_stable = PerformanceAnalyser.check_stability(algorithm)

        return pd.DataFrame(
            data={'Comparisons on sorted data': [comparisons_sorted],
                  'Comparisons on reversed data': [comparisons_reversed],
                  'Comparisons on shuffled data': [comparisons_shuffled],
                  'is_stable': is_stable})
