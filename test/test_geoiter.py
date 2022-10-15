import pickle

import pytest

from geoiter import GeoIter
from geoiter.util.ressource_example import get_german_border


@pytest.fixture()
def nodes():
    return [
        (1, 1), (2, 1), (2, 2), (1, 2)
    ]


@pytest.fixture()
def simple_geo(nodes):
    return GeoIter(boundary=nodes, radius=1)


@pytest.fixture()
def germany():
    return get_german_border()


@pytest.fixture()
def iter_germany(germany):
    return GeoIter(boundary=germany, radius=100)


class TestGeoIter:
    def test_center(self, nodes):
        geo = GeoIter(boundary=nodes, radius=1)
        c = geo.center
        assert c == (1.5, 1.5)

    def test_west(self, simple_geo):
        assert simple_geo._west_of_median == [(1, 1), (2, 1)]

    def test_east(self, simple_geo):
        assert simple_geo._east_of_median == [(1, 2), (2, 2)]

    def test_center2(self, iter_germany):
        geo = iter_germany
        assert geo.center == (51.1846362, 10.4541231)

    def test_intersect_lat_west(self, iter_germany):
        coordinate = iter_germany.boundary[len(iter_germany.boundary) // 2]
        first = iter_germany._intersect_lat_west(coordinate)
        assert iter_germany._intersect_lat_west(coordinate) == (49.941555, 6.22151)

    def test_iter(self, iter_germany):
        l = list(iter_germany)  # 86ms
        l = list(iter_germany)  # 86 ms
        l = list(iter_germany)  # 89 ms
        assert len(l) == 18
        # 541 # 68 ms

    def test__generator(self, iter_germany):
        g = iter_germany._generator()
        next(g)

    def test_compressor(self, germany, benchmark):
        i10 = GeoIter(germany, radius=100, comp_rate=10)
        i1 = GeoIter(germany, radius=100, comp_rate=1)
        assert len(i1.boundary) > len(i10.boundary)

    def test_benchmark_compressor_1(self, germany, benchmark):
        i10 = GeoIter(germany, radius=100, comp_rate=1)
        benchmark(lambda: list(i10))
        # 1,4 s

    def test_benchmark_compressor_10(self, germany, benchmark):
        i10 = GeoIter(germany, radius=100, comp_rate=10)
        benchmark(lambda: list(i10))
        # 81 ms


class TestVisual:
    # this a hack to avoid problems with pytest and debuging
    try:
        from geoiter.util.plot import plot_geoiter
    except Exception as e:
        raise ImportError("Please install plot extension via pip install geoiter['plot']")

    def test_and_plot(self, iter_germany):
        geo = iter_germany
        assert geo.center == (51.1846362, 10.4541231)
        TestVisual.plot_geoiter(geo)
