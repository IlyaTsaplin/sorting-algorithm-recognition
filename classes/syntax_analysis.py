import ast
import pandas as pd


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
