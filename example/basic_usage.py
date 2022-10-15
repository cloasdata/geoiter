import pickle

from geoiter.util.ressource_example import get_german_border
from geoiter import GeoIter

# get you boundary
germany = get_german_border()

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

