# geoiter
iterates the planet.

A simple tool to iterate circles within given boundaries:
![grid_germany](https://user-images.githubusercontent.com/84661606/159547536-a05af9ac-b2ed-43d6-a5fd-ff8bb82a5466.png)

**geoiter** can be used for web scraping to utilize geo/location queries.
![result](https://user-images.githubusercontent.com/84661606/159547610-ae9656c4-6771-4a39-ae39-f88826b1998c.png)

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

