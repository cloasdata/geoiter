"""
Demonstrate the plot extension
"""

import pickle
from geoiter import GeoIter
from geoiter.util.ressource_example import get_german_border

# to use this: pip install geoiter["plot"]
# please note this may not work on windows machine. Please load GEOS/Cartopy binaries manual.
# cartopy is base on GEOS.

from geoiter.util.plot import  plot_geoiter

# get you boundaries
germany = get_german_border()

# prepare
gi = GeoIter(
    boundary=germany,
    radius=100,
    comp_rate=20
    )

# plot
plot_geoiter(gi)