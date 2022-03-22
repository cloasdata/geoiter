"""
Provide gpx ulities to export in a .gpx format.
"""
try:
    from lxml.builder import ElementMaker
    from lxml.etree import tostring
except ImportError as e:
    args = e.args
    e.args = (*args, "Please install plot extension: pip install geoiter['gpx']")
    raise


from geoiter.geoiter import Coordinates


def gpx_prepare(coordinates: Coordinates):
    """
    Builds the xml tree for the gpx file
    """
    # header/meta
    namespace = "http://www.topografix.com/GPX/1/1"

    elements = ElementMaker(namespace=namespace, nsmap={None: namespace})

    root = elements.gpx(version="1.1", creator="gpx_dumps")
    root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
             f"{namespace} http://www.topografix.com/GPX/1/1/gpx.xsd")
    root.append(elements.metadata(elements.name("grid")))

    # add coordinates as waypoints
    for c in coordinates:
        root.append(
            elements.wpt(
                lat=str(c[0]),
                lon=str(c[1]),
            )

        )
    return root


def gpx_dumps(coordinates: Coordinates) -> bin:
    gpx = gpx_prepare(coordinates)
    return tostring(gpx, encoding="utf-8")


def gpx_dump(coordinates: Coordinates, file):
    file.write(gpx_dumps(coordinates))
