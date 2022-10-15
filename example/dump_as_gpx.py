import pickle
from geoiter import GeoIter

from geoiter.util.ressource_example import get_germany_boundary

# to use this example install pip install geoiter["gpx"]
from geoiter.util.gpx import gpx_dumps

# get you boundaries
germany = get_germany_boundary()

# prepare
gi = GeoIter(
    boundary=germany,
    radius=100,
    comp_rate=20
    )
coordinates = list(gi)

gpx = gpx_dumps(coordinates)

print(gpx)
