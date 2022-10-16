# geoiter
iterates the planet.

A simple tool to iterate coordinates within given boundaries such as country boundary.
The usage is mostly for querying/searching by location at for example ebay.com or zillow.com
A better description can be found <a ref="https://cloasdata.de/?p=321">here</a>.
 
Let's say Germany has in sum 5000 houses to sell. Then most platforms will only allow you to visit or request the first 200 houses. 
Now to get the others, you need to dissect the big boundary area into smaller ones.
And this is where geoiter provides you with coordinates.

<img src="https://user-images.githubusercontent.com/84661606/159549731-44de6016-0582-4ef2-94ba-646b6277aec3.png" width="300" />


**geoiter** can be used for web scraping to utilize geo/location queries:

<img src="https://user-images.githubusercontent.com/84661606/159549754-470fa19f-a826-44ad-b76c-6c338ae72b1b.png" width="300"/>

In many cases the web page restrict the result items to a fixed number. 
With geoiter you can now dissect this one query to a many location queries to relax 
the result density under the restriction limit.

geoiter has only one additional dependency called [haversine](https://pypi.org/project/haversine/).

## Install
    pip install geoiter


## Usage

```python
from geoiter.util.ressource_example import get_german_border
from geoiter import GeoIter

# get you boundary for example
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
```

You can find more samples under /example. There is also a real life we scraper.

## Speed
one may consider that geo data have megabytes of coordinates. Which may make the iteration very slow,
because it needs to look up coordinates in the boundary often.
To accelerate the **geoiter** provides a very simple compressor and uses bisect instead of list iteration.
However, it still can be slow.

## Extensions
There two extensions which give additional help

    pip install geoiter["gpx"]

provides you with an gpx exporter.

    pip install geoiter["plot"]

provides a plotting function to visualize the grid.

## Data for borders
get boundaries from osm or others sources like
* https://www.geoboundaries.org/
* https://osm-boundaries.com/
* ...

## Todo
* SRP for compressor
* Make own haversine calculation for fixed directions.

## Homepage
* <a href="https://github.com/cloasdata/geoiter">on github</a>
* <a href="https://pypi.org/project/geoiter">on pypi</a>
* <a href="https://cloasdata.de/?p=321">on my homepage</a>