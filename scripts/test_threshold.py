import argparse
import pickle
import traceback
from pathlib import Path

import numpy as np

from classes.exceptions import IncorrectSorting, ErrorInSorting, NoSortMethod
from config import PREDICTION_THRESHOLD
from scripts.train_forest import get_algorithm_characteristics

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Test threshold parameter for dataset and classifier')
    parser.add_argument('--dataset', help='Path to dataset of sorting algorithms')
    parser.add_argument('--classifier', help='Path to trained classifier')
    args = parser.parse_args()

    loaded_model = pickle.load(open(Path(args.classifier) / 'forest.clf', 'rb'))
    label_encoder = pickle.load(open(Path(args.classifier) / 'label_encoder.pkl', 'rb'))
    predictions = []
    for path in Path(args.dataset).iterdir():
        if path.is_dir() and path.name in label_encoder.classes_:
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

                prediction = loaded_model.predict_proba(current_implementation_df)
                current_prediction = np.max(prediction[0])
                if current_prediction < PREDICTION_THRESHOLD:
                    print(implementation.name)
                    print("Unknown algorithm")
                    for i, val in enumerate(prediction[0]):
                        print(f"{label_encoder.inverse_transform([i])[0]} - {round(val * 100, 4)}%")
                    print("---------------------------------------------")
                predictions.append(current_prediction)

    print(f"Average percentage: {round(np.average(predictions) * 100, 4)}%")
