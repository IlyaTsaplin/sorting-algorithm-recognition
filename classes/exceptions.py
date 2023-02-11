class ErrorInSorting(Exception):
    """
    Errors occurred during execution
    """
    def __init__(self):
        message = (
            "Error occurred during execution of source code\n"
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
    def __init__(self):
        message = (
            "Sorting algorithm is incorrect\n"
        )
        super().__init__(message)
