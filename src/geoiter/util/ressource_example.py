# gives some example data to test around with

from pathlib import Path
import pickle

path_to_germany = Path(__file__).parent / "res" / "germany.obj"


def get_germany_boundary():
    return pickle.load(path_to_germany.open("rb"))

