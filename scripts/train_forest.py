import argparse
import pickle
import traceback
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.experimental import enable_halving_search_cv  # noqa
from sklearn.model_selection import cross_val_score, RepeatedKFold, HalvingGridSearchCV

from classes.exceptions import ErrorInSorting, NoSortMethod, IncorrectSorting
from classes.performance_analysis import PerformanceAnalyser
from classes.syntax_analysis import SyntaxAnalyser
from config import ALGORITHMS


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


def collect_data(path_to_data):
    sorting_df = pd.DataFrame()

    # Iterate over different directories for different sorting algorithms
    for path in path_to_data.iterdir():
        if path.is_dir() and path.name in ALGORITHMS:
            current_algorithm_df = pd.DataFrame()
            implementations = path.glob('*.py')

            # Iterate over implementations
            for implementation in implementations:
                try:
                    current_implementation_df = get_algorithm_characteristics(implementation)
                except IncorrectSorting as e:
                    # Handle incorrect algorithm
                    print(f'Sorting algorithm from {implementation} is not correct')
                    print(e)
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

    return sorting_df


def train_classifier(dataset_path, output_path):
    # Collect data from implementations dataset
    path_to_data = Path(dataset_path)
    sorting_df = collect_data(path_to_data)

    if len(sorting_df) != 0:
        algorithms = sorted(list(sorting_df['sorting_algorithm'].unique()))
        targets = []
        for value in sorting_df['sorting_algorithm'].values:
            index = algorithms.index(value)
            targets.append(index)
        test = sorting_df.drop(['sorting_algorithm', 'filename'], axis=1)

        param_grid = {'max_depth': [3, 4, 5, 7, 9]}
        base_estimator = RandomForestClassifier()
        sh = HalvingGridSearchCV(base_estimator, param_grid, cv=5,
                                 factor=2, resource='n_estimators',
                                 max_resources=100).fit(test, targets)
        clf = sh.best_estimator_
        print(clf)

        # Validation
        scores = cross_val_score(clf, test, targets, cv=RepeatedKFold(n_splits=5, n_repeats=20))
        print(scores.mean())

        # Plot classifier
        # clf = clf.fit(test, targets)
        # for tree in clf.estimators_:
        #     _ = plt.figure(figsize=(15, 20))
        #     _ = plot_tree(tree, filled=True, feature_names=test.columns, class_names=algorithms)
        #     plt.show()

        pickle.dump(clf, open(Path(output_path), 'wb'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Train random forest classifier')
    parser.add_argument('--dataset', help='Path to dataset of sorting algorithms')
    parser.add_argument('--output', help='Path for saving trained classifier')
    args = parser.parse_args()
    train_classifier(args.dataset, args.output)
