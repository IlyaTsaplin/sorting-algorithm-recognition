import ast
from classes.recursive_functions_finder import RecursiveFunctionsFinder


class SyntaxAnalyser:
    """
    Class for syntax analysis of sorting algorithms
    """
    @staticmethod
    def get_recursive_functions(code):
        """
        Get all recursive functions from code
        :param code: Python code string
        :return: Set of function names that are recursive
        """
        tree = ast.parse(code)
        finder = RecursiveFunctionsFinder()
        finder.visit(tree)
        return finder.recursive_funcs
