import copy
import pandas as pd
from classes.element import Element
from classes.exceptions import ErrorInSorting, IncorrectSorting


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
    nearly_sorted_elements = [1, 2, 0, 7, 3, 5, 6, 4, 8, 9, 10, 12, 13, 11, 15, 14, 17, 16, 18, 19, 20, 21, 22, 24, 23,
                              25, 27, 29, 26, 28, 30, 32, 31, 34, 33, 36, 35, 37, 38, 43, 41, 40, 42, 39, 44, 46, 45,
                              47, 49, 48, 51, 50, 52, 54, 53, 55, 57, 56, 58, 59, 60, 62, 64, 61, 63, 66, 65, 67, 68,
                              69, 71, 70, 72, 73, 74, 75, 79, 76, 77, 80, 83, 82, 81, 78, 85, 84, 87, 86, 88, 89, 92,
                              91, 90, 94, 93, 95, 97, 96, 98, 99]

    ordered_data = [Element(x, x) for x in range(100)]
    shuffled_data = [Element(shuffled_element, i) for i, shuffled_element in enumerate(shuffled_elements)]
    nearly_sorted_data = [Element(x, i) for i, x in enumerate(nearly_sorted_elements)]
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
        except Exception:
            raise ErrorInSorting()

        if not cls.is_sorted(data):
            raise IncorrectSorting()

        return Element.comparison_counter

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
        except Exception:
            raise ErrorInSorting()

        if not cls.is_sorted(data):
            raise IncorrectSorting()
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
        :return: Dataframe containing performance characteristics
        """
        collected_data = pd.DataFrame()

        collected_data['Comparisons on sorted data'] = [PerformanceAnalyser.count_comparisons(algorithm,
                                                                                              cls.ordered_data)]
        collected_data['Comparisons on reversed data'] = PerformanceAnalyser.count_comparisons(algorithm,
                                                                                               cls.ordered_data[::-1])
        collected_data['Comparisons on shuffled data'] = PerformanceAnalyser.count_comparisons(algorithm,
                                                                                               cls.shuffled_data)
        collected_data['Comparisons on nearly sorted data'] = PerformanceAnalyser. \
            count_comparisons(algorithm, cls.nearly_sorted_data)
        collected_data['is_stable'] = PerformanceAnalyser.check_stability(algorithm)

        return collected_data
