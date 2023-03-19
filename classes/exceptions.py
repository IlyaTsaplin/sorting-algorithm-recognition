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
