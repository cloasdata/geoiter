# geoiter
iterates the planet.

A simple tool to iterate circles within given boundaries:

<img src="https://user-images.githubusercontent.com/84661606/159549731-44de6016-0582-4ef2-94ba-646b6277aec3.png" width="300" />


**geoiter** can be used for web scraping to utilize geo/location queries:

<img src="https://user-images.githubusercontent.com/84661606/159549754-470fa19f-a826-44ad-b76c-6c338ae72b1b.png" width="300"/>

In many cases the web page restrict the result items to a fixed number. 
With geoiter you can now dissect this one query to a many location queries to relax 
the result density under the restriction limit.

geoiter has only one additional dependency called [haversine](https://pypi.org/project/haversine/).

## install
    pip install geoiter

## usage
```python
import pickle

from geoiter.util.ressource_example import germany
from geoiter import GeoIter

# get you boundary for example
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
```
## speed
one may consider that geo data have mb of coordinates. Which may make the this iteration very slow,
because it needs to look up coordinates in the boundary often.
To accelerate the **geoiter** provides a very simple compressor and uses bisect instead of list iteration.
However, it still can be slow.

## extensions
There two extensions which give additional help

    pip install geoiter["gpx]

provides you with an gpx exporter.

    pip install geoiter["plot"]

provides a plotting function to visualize the grid.

## data
get boundaries from osm or others sources like
* https://www.geoboundaries.org/
* https://osm-boundaries.com/
* ...

