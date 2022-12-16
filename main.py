import pandas as pd
from pathlib import Path
from sklearn import tree
from classes.performance_analyser import PerformanceAnalyser, ErrorInSorting
from classes.syntax_analyser import SyntaxAnalyser
from matplotlib import pyplot as plt


def get_algorithm_characteristics(path_to_algorithm: Path):
    """
    Extracts performance and syntax characteristics of given sorting algorithm
    params
    """
    module = __import__(f'{".".join(path_to_algorithm.parts[:-1])}.{path_to_algorithm.stem}',
                        fromlist=['sort'])

    characteristics_df = PerformanceAnalyser.measure_algorithm(getattr(module, 'sort'))

    # Syntax
    with open(path_to_algorithm) as in_stream:
        code = in_stream.read()
        characteristics_df['is_recursive'] = SyntaxAnalyser.get_recursive_functions(code) != set()

    return characteristics_df


def main():
    sorting_df = pd.DataFrame()
    path_to_data = Path('./data')
    for path in path_to_data.iterdir():
        if path.is_dir():
            performance_df = pd.DataFrame()

            for implementation in path.glob('*.py'):
                try:
                    current_df = get_algorithm_characteristics(implementation)
                except AssertionError:
                    # Handle incorrect algorithm
                    print(f'Sorting algorithm from {implementation} is not correct')
                    continue
                except AttributeError:
                    # Handle missing sort function
                    print(f'Sorting algorithm from {implementation} is missing sort function')
                    continue
                except ErrorInSorting:
                    raise ErrorInSorting
                performance_df = pd.concat([performance_df, current_df])

            performance_df = performance_df.assign(sorting_algorithm=path.name)
            sorting_df = pd.concat([sorting_df, performance_df])

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(sorting_df)

    if len(sorting_df) != 0:
        y = sorting_df['sorting_algorithm']
        X = sorting_df.drop('sorting_algorithm', axis=1)
        clf = tree.DecisionTreeClassifier(max_depth=5)
        clf = clf.fit(X, y)
        _ = plt.figure(figsize=(15, 20))
        _ = tree.plot_tree(clf, filled=True,
                           feature_names=X.columns, class_names=list(y))
        plt.show()


if __name__ == '__main__':
    main()
