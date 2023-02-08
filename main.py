import pandas as pd
from pathlib import Path
from sklearn import tree
from sklearn.model_selection import cross_val_score, RepeatedKFold
from classes.performance_analyser import PerformanceAnalyser, ErrorInSorting
from classes.syntax_analyser import SyntaxAnalyser
from matplotlib import pyplot as plt


PATH_TO_IMPLEMENTATIONS = './data'


def get_algorithm_characteristics(path_to_algorithm: Path):
    """
    Extracts performance and syntax characteristics of given sorting algorithm
    @param path_to_algorithm: path to source code of sorting algorithm
    @return: Dataframe containing algorithm characteristics
    """
    module = __import__(f'{".".join(path_to_algorithm.parts[:-1])}.{path_to_algorithm.stem}',
                        fromlist=['sort'])

    characteristics_df = PerformanceAnalyser.measure_algorithm(getattr(module, 'sort'))

    # Syntax
    with open(path_to_algorithm) as in_stream:
        code = in_stream.read()
        characteristics_df['is_recursive'] = 'sort' in SyntaxAnalyser.get_recursive_functions(code)

    return characteristics_df


def main():
    # Collect data from implementations dataset
    sorting_df = pd.DataFrame()
    path_to_data = Path(PATH_TO_IMPLEMENTATIONS)

    # Iterate over different directories for different soring algorithms
    for path in path_to_data.iterdir():
        if path.is_dir():
            performance_df = pd.DataFrame()
            implementations = path.glob('*.py')
            current_df = None

            # Iterate over implementations
            for implementation in implementations:
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
                current_df['filename'] = implementation.name
                performance_df = pd.concat([performance_df, current_df])

            if current_df is not None:
                performance_df = performance_df.assign(sorting_algorithm=path.name)
                sorting_df = pd.concat([sorting_df, performance_df])

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(sorting_df)

    if len(sorting_df) != 0:
        algorithms = list(sorting_df['sorting_algorithm'].unique())
        targets = []
        for value in sorting_df['sorting_algorithm'].values:
            index = algorithms.index(value)
            targets.append(index)
        test = sorting_df.drop(['sorting_algorithm', 'filename'], axis=1)
        clf = tree.DecisionTreeClassifier(max_depth=4)

        scores = cross_val_score(clf, test, targets, cv=RepeatedKFold(n_splits=5,  n_repeats=20))

        print(scores)
        print(scores.mean())

        clf = clf.fit(test, targets)
        _ = plt.figure(figsize=(15, 20))
        _ = tree.plot_tree(clf, filled=True, feature_names=test.columns, class_names=algorithms)
        plt.show()


if __name__ == '__main__':
    main()
