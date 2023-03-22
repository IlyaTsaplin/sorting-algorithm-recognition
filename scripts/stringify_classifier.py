import argparse
import pickle
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert classifier to txt')
    parser.add_argument('--classifier', help='Path to trained classifier')
    args = parser.parse_args()

    loaded_model = pickle.load(open(Path(args.classifier) / 'forest.clf', 'rb'))
    string = str(pickle.dumps(loaded_model, 0))
    with open(Path(args.classifier) / 'forest.txt', "w") as text_file:
        text_file.write(repr(string))

    loaded_encoder = pickle.load(open(Path(args.classifier) / 'label_encoder.pkl', 'rb'))
    string = str(pickle.dumps(loaded_encoder, 0))
    with open(Path(args.classifier) / 'label_encoder.txt', "w") as text_file:
        text_file.write(repr(string))
