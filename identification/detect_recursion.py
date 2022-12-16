import ast
from classes.recursive_functions_finder import RecursiveFunctionsFinder


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


def main():
    algorithms = ['mergesort', 'insertionsort', 'quicksort', 'timsort']
    for name in algorithms:
        with open(f'./sorting_algorithms/{name}.py') as in_stream:
            code = in_stream.read()
            print(f'Recursive functions in {name}:')
            print(get_recursive_functions(code))


if __name__ == '__main__':
    main()
