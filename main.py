import pandas as pd
import traceback
import pickle
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import cross_val_score, RepeatedKFold
from classes.performance_analysis import PerformanceAnalyser
from classes.syntax_analysis import SyntaxAnalyser
from classes.exceptions import ErrorInSorting, NoSortMethod, IncorrectSorting
from matplotlib import pyplot as plt


PATH_TO_IMPLEMENTATIONS = './data'
CLASSIFIER_NAME = 'tree.clf'
PATH_TO_TEST = './data/test.py'
ALGORITHMS = ['bubble_sort', 'timsort', 'selection_sort', 'insertion_sort', 'merge_sort', 'quicksort', 'default_sort']


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


def train_classifier():
    # Collect data from implementations dataset
    sorting_df = pd.DataFrame()
    path_to_data = Path(PATH_TO_IMPLEMENTATIONS)

    # Iterate over different directories for different sorting algorithms
    for path in path_to_data.iterdir():
        if path.is_dir() and path.name in ALGORITHMS:
            current_algorithm_df = pd.DataFrame()
            implementations = path.glob('*.py')

            # Iterate over implementations
            for implementation in implementations:
                try:
                    current_implementation_df = get_algorithm_characteristics(implementation)
                except IncorrectSorting:
                    # Handle incorrect algorithm
                    print(f'Sorting algorithm from {implementation} is not correct')
                    continue
                except NoSortMethod:
                    # Handle missing sort function
                    print(f'Sorting algorithm from {implementation} is missing sort function')
                    continue
                except ErrorInSorting as e:
                    # Handle error in provided source code
                    print(f'Sorting algorithm  {implementation} raised an exception')
                    print(e)
                    traceback.print_exc()
                    continue

                current_implementation_df['filename'] = implementation.name
                current_algorithm_df = pd.concat([current_algorithm_df, current_implementation_df])

            current_algorithm_df = current_algorithm_df.assign(sorting_algorithm=path.name)
            current_algorithm_df['is_stable'] = current_algorithm_df['is_stable'].astype(bool)
            current_algorithm_df['is_recursive'] = current_algorithm_df['is_recursive'].astype(bool)
            sorting_df = pd.concat([sorting_df, current_algorithm_df])

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(sorting_df)

    if len(sorting_df) != 0:
        algorithms = list(sorting_df['sorting_algorithm'].unique())
        targets = []
        for value in sorting_df['sorting_algorithm'].values:
            index = algorithms.index(value)
            targets.append(index)
        test = sorting_df.drop(['sorting_algorithm', 'filename'], axis=1)
        clf = DecisionTreeClassifier()
        print(algorithms)
        scores = cross_val_score(clf, test, targets, cv=RepeatedKFold(n_splits=5,  n_repeats=20))

        print(scores)
        print(scores.mean())

        # Plot classifier
        clf = clf.fit(test, targets)
        _ = plt.figure(figsize=(15, 20))
        _ = plot_tree(clf, filled=True, feature_names=test.columns, class_names=algorithms)
        plt.show()

        pickle.dump(clf, open(Path(PATH_TO_IMPLEMENTATIONS) / CLASSIFIER_NAME, 'wb'))


def test_classifier():
    loaded_model = pickle.load(open(Path(PATH_TO_IMPLEMENTATIONS) / CLASSIFIER_NAME, 'rb'))
    characteristics = get_algorithm_characteristics(Path(PATH_TO_TEST))
    print(ALGORITHMS[loaded_model.predict(characteristics)[0]])


if __name__ == '__main__':
    train_classifier()
