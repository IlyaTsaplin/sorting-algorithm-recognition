import ast
import copy
import subprocess
import sys
from pathlib import Path

import sklearn
import pandas as pd


# Element
class Element:
    """
    Class that keeps count of how many times instances were compared
    """
    comparison_counter = 0

    @classmethod
    def reset_counter(cls):
        cls.comparison_counter = 0

    def __init__(self, sorting_criteria, sequential_id):
        self.sorting_criteria = sorting_criteria
        self.sequential_id = sequential_id

    def __lt__(self, other):
        Element.comparison_counter += 1
        return self.sorting_criteria < other.sorting_criteria

    def __gt__(self, other):
        Element.comparison_counter += 1
        return self.sorting_criteria > other.sorting_criteria

    def __le__(self, other):
        Element.comparison_counter += 1
        return self.sorting_criteria <= other.sorting_criteria

    def __ge__(self, other):
        Element.comparison_counter += 1
        return self.sorting_criteria >= other.sorting_criteria

    def __eq__(self, other):
        Element.comparison_counter += 1
        return self.sorting_criteria == other.sorting_criteria

    def __ne__(self, other):
        Element.comparison_counter += 1
        return self.sorting_criteria != other.sorting_criteria

    def __floordiv__(self, other):
        return self.sorting_criteria // other


# Performance analyser
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
        sorted_data = copy.deepcopy(data)
        Element.reset_counter()

        try:
            sorting_algorithm(sorted_data)
        except Exception as e:
            raise ErrorInSorting(e)

        if not cls.is_sorted(sorted_data):
            raise IncorrectSorting(data, sorted_data)

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
        sorted_data = cls.stable_check_data.copy()

        try:
            sorting_algorithm(sorted_data)
        except Exception as e:
            raise ErrorInSorting(e)

        if not cls.is_sorted(sorted_data):
            raise IncorrectSorting(cls.stable_check_data, sorted_data)
        return PerformanceAnalyser.sequential_are_ascending(sorted_data)

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


# Exceptions
class ErrorInSorting(Exception):
    """
    Errors occurred during execution
    """

    def __init__(self, exception):
        self.exception = exception

        message = (
            "Error occurred during execution of source code\n"
            f"{self.exception}\n"
        )
        super().__init__(message)


class NoSortMethod(Exception):
    """
    Method called sort is missing in source code
    """

    def __init__(self, path_to_source):
        message = (
            "No method sort was found in source code\n"
            f"Path to source code: {path_to_source}\n"
        )
        self.path_to_source = path_to_source
        super().__init__(message)


class IncorrectSorting(Exception):
    """
    Provided sorting algorithm is incorrect
    """

    def __init__(self, input_data, incorrect_result):
        message = (
            "Sorting algorithm is incorrect\n"
            f"Input data: {[elem.sorting_criteria for elem in input_data]}\n"
            f"Correct result: {[elem.sorting_criteria for elem in sorted(input_data)]}\n"
            f"Incorrect result: {[elem.sorting_criteria for elem in incorrect_result]}\n"
        )
        super().__init__(message)


# Syntax analyser
class SyntaxAnalyser:
    """
    Class for syntax analysis of sorting algorithms
    """

    class RecursiveFunctionsFinder(ast.NodeVisitor):
        """
        AST node visitor for finding recursive functions
        """

        def __init__(self):
            self._current_func = None
            self.recursive_funcs = set()

        def generic_visit(self, node):
            if node.__class__ is ast.FunctionDef:
                self._current_func = node.name
            if node.__class__ is ast.Call and hasattr(node.func, 'id') and node.func.id == self._current_func:
                self.recursive_funcs.add(self._current_func)
            super(self.__class__, self).generic_visit(node)

    class CycleCounter(ast.NodeVisitor):
        """
        Class for counting cycles in code
        """

        def __init__(self):
            self.cycles = 0
            self.nested_cycles = 0

        def generic_visit(self, node):
            # Iterate over For and While elements
            if (node.__class__ is ast.For) or (node.__class__ is ast.While):
                self.cycles += 1

                # Count nested cycles inside current cycle
                for inner_node in node.body:
                    if (inner_node.__class__ is ast.For) or (inner_node.__class__ is ast.While):
                        self.nested_cycles += 1

            super(self.__class__, self).generic_visit(node)

    @staticmethod
    def get_recursive_functions(code):
        """
        Get all recursive functions from code
        :param code: Python code string
        :return: Set of function names that are recursive
        """
        tree = ast.parse(code)
        finder = SyntaxAnalyser.RecursiveFunctionsFinder()
        finder.visit(tree)
        return finder.recursive_funcs

    @staticmethod
    def count_cycles(code):
        """
        Count all for and while cycles in code
        @param code: Python code string
        @return: Tuple (number_of_cycles, number_of_inner_cycles)
        """
        tree = ast.parse(code)
        cycle_counter = SyntaxAnalyser.CycleCounter()
        cycle_counter.visit(tree)
        return cycle_counter.cycles, cycle_counter.nested_cycles

    @staticmethod
    def analyze(code):
        """
        Extract syntax characteristics from Python code string
        @param code: Python code string
        @return: Dataframe containing syntax characteristics
        """
        syntax_characteristics = pd.DataFrame()

        syntax_characteristics['is_recursive'] = [len(SyntaxAnalyser.get_recursive_functions(code)) != 0]
        cycles, nested_cycles = SyntaxAnalyser.count_cycles(code)
        syntax_characteristics['number_of_cycles'] = [cycles]
        syntax_characteristics['number_of_nested_cycles'] = [nested_cycles]

        return syntax_characteristics


def get_algorithm_characteristics(path_to_algorithm: Path):
    """
    Extracts performance and syntax characteristics of given sorting algorithm
    @param path_to_algorithm: path to source code of sorting algorithm
    @return: Dataframe containing algorithm characteristics
    """
    try:
        module = __import__(f'{".".join(path_to_algorithm.parts[:-1])}.{path_to_algorithm.stem}',
                            fromlist=['sort'])
    except AttributeError:
        raise NoSortMethod(Path)

    performance_characteristics = PerformanceAnalyser.measure_algorithm(getattr(module, 'sort'))

    # Syntax
    with open(path_to_algorithm) as in_stream:
        code = in_stream.read()
        syntax_characteristics = SyntaxAnalyser.analyze(code)

        all_characteristics = performance_characteristics.join(syntax_characteristics)

    return all_characteristics


def predict_sorting(characteristics):
    # TODO add trained classifier
    return "quick_sort"


EXPECTED_SORTING = "quick_sort"

lines = """{{ STUDENT_ANSWER | e('py') }}"""
# checking with inspect

with open("prog.py", "w") as src:
    print(lines, file=src)

try:
    characteristics = get_algorithm_characteristics(Path("prog.py"))
except subprocess.CalledProcessError as e:
    if e.returncode > 0:
        # Ignore non-zero positive return codes
        if e.output:
            print(e.output)
    else:
        # But negative return codes are signals - abort
        if e.output:
            print(e.output, file=sys.stderr)
        if e.returncode < 0:
            print("Task failed with signal", -e.returncode, file=sys.stderr)
        print("** Further testing aborted **", file=sys.stderr)

print(predict_sorting(characteristics))
