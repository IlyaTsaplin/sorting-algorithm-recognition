import argparse
import pickle
import traceback
from pathlib import Path

import numpy as np

from classes.exceptions import ErrorInSorting, NoSortMethod, IncorrectSorting
from config import ALGORITHMS, PREDICTION_THRESHOLD
from scripts.train_forest import get_algorithm_characteristics

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Predict sorting algorithm from source code')
    parser.add_argument('--input', help='Path file with source code')
    parser.add_argument('--classifier', help='Path to trained classifier')
    args = parser.parse_args()

    loaded_model = pickle.load(open(Path(args.classifier), 'rb'))
    try:
        characteristics = get_algorithm_characteristics(Path(args.input))
    except IncorrectSorting as e:
        # Handle incorrect algorithm
        print(f'Sorting algorithm is not correct')
        print(e)
    except NoSortMethod:
        # Handle missing sort function
        print(f'Sorting algorithm is missing sort function')
    except ErrorInSorting as e:
        # Handle error in provided source code
        print(f'Sorting algorithm raised an exception')
        print(e)
        traceback.print_exc()
    else:
        prediction = loaded_model.predict_proba(characteristics)
        if np.max(prediction[0]) > PREDICTION_THRESHOLD:
            print(f"{ALGORITHMS[np.argmax(prediction[0])]} - {round(np.max(prediction[0]) * 100, 2)}%")
        else:
            print("Unknown algorithm")
            for i, val in enumerate(prediction[0]):
                print(f"{ALGORITHMS[i]} - {round(val * 100, 2)}%")
