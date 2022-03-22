try:
    import cartopy.crs as ccrs
    import cartopy.geodesic as geodesic
    from cartopy.feature import BORDERS, COASTLINE
    from shapely.geometry import Polygon
    from descartes import PolygonPatch

    import matplotlib.pyplot as plt
except ImportError as e:
    args = e.args
    e.args = (*args, "Please install plot extension: pip install geoiter['plot']")
    raise

from geoiter import GeoIter, Coordinate, Coordinates


def plot_geoiter(geo_iter: GeoIter):
    """
    Plots the Geooiter
    :param geo_iter:
    :return:
    """
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([4, 16, 56, 47], crs=ccrs.PlateCarree())
    GRAY = '#999999'
    for coordinate in geo_iter:
        circle_points = geodesic.Geodesic().circle(coordinate[1], coordinate[0], geo_iter.radius * 1_000)
        geom = Polygon(circle_points)
        patch = PolygonPatch(geom, fc=GRAY, ec=GRAY, alpha=0.5)
        ax.add_patch(patch)
        # ax.add_geometries((patch,), crs=cartopy.crs.PlateCarree(), facecolor='red', edgecolor='none', linewidth=0)

    ax.add_feature(BORDERS)
    ax.add_feature(COASTLINE)

    plt.show()  #


def circle_as_boundary(center: Coordinate, radius_km) -> Coordinates:
    """Helper to provide nice circles"""
    circles = geodesic.Geodesic().circle(center[1], center[0], radius_km * 1_000)
    circles[:, [1, 0]] = circles[:, [0, 1]]
    return circles.tolist()
