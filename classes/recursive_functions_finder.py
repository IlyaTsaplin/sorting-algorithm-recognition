import ast


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
        super(RecursiveFunctionsFinder, self).generic_visit(node)
