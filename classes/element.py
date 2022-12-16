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
