import pickle

from geoiter.util.ressource_example import germany
from geoiter import GeoIter

# get you boundary
with open(germany, "rb") as file:
    germany = pickle.load(file)

# prepare
gi = GeoIter(
    boundary=germany,
    radius=100,
    comp_rate=20
    )

if __name__ == "__main__":
    # plot them as example
    for coordinate in gi:
        print(coordinate)

