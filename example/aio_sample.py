# main.py
import asyncio
import httpx  # or any other popular http client.
from lxml.html import fromstring  # or use bs4

from geoiter.util.ressource_example import get_german_border
# this is a example list of coordinates. You may get you own from open street map or other geospatial services.
from geoiter import GeoIter

german_border = get_german_border()

query_radius = 30

gi = GeoIter(
    boundary=german_border,
    radius=query_radius,
    comp_rate=20
)

midpoints = list(gi)  # consume that iterator at once
print(len(midpoints), midpoints[:2])

base_url = r"https://www.autoscout24.com/lst/volkswagen/golf-(" \
           r"all)?sort=standard&desc=0&atype=C&ustate=N%2CU&powertype=kw "


def parse_offers(body_tree):
    articles = body_tree.xpath("//article")
    for article in articles:
        title = article.xpath(".//h2/text()")[0]
        price = article.xpath(".//p/text()")[0]
        print(title, price)


async def fetch_page(client, query_url):
    response = await client.get(query_url)
    body_tree = fromstring(response.text)
    parse_offers(body_tree)


async def fetch_query_coro(client, query_url, loop):
    response = await client.get(query_url)
    assert response.status_code == 200
    body_tree = fromstring(response.text)
    query_size = body_tree.xpath("//div[@class='ListHeader_top__jY34N']/h1/span/span/text()")[0]
    if query_size:
        parse_offers(body_tree)
        more_pages = int(query_size) // 20
        print(f"I need to scrape now {query_size} offers or {more_pages} more page(s).")

        pending = set()
        for page in range(1, more_pages + 1):
            pending.add(
                loop.create_task(fetch_page(client, query_url + f"&page={page + 1}"))
            )
        done, pending = await asyncio.wait(pending)


async def main():
    client = httpx.AsyncClient()
    loop = asyncio.get_event_loop()
    async with client:
        pending = []
        for coordinate in midpoints[100:102]:
            query_url = f"{base_url}&lon={coordinate[1]}&lat={coordinate[0]}&zipr={query_radius}"
            pending.append(
                loop.create_task(fetch_query_coro(client, query_url, loop))
            )
        done, pending = await asyncio.wait(pending)


if __name__ == '__main__':
    asyncio.run(main(), debug=True)
