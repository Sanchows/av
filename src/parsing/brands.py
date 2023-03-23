from dataclasses import dataclass
import json

from bs4 import BeautifulSoup as bs

from parsing import client


@dataclass
class Brand:
    brand_id: int  # 42
    url: str  # https://cars.av.by/chrysler
    label: str  # Chrysler
    count: int  # 308 (dynamic) probably it's not necessary field


async def get_brands() -> tuple[Brand]:
    brands = await _parse_brands()

    return brands


async def _parse_brands() -> tuple[Brand]:
    response = await client.get_brands()

    _raw_script = bs(response.text, "lxml").find("script", id="__NEXT_DATA__")
    brands_with_id = _get_brands_with_id(_raw_script)

    brands_with_links = _get_brands_with_links(_raw_script)

    brands = (
        item[0] | item[1] for item in zip(brands_with_links, brands_with_id)
    )

    return tuple(
        Brand(
            brand_id=item["id"],
            url=item["url"],
            label=item["label"],
            count=item["count"],
        )
        for item in brands
    )


def _get_brands_with_id(raw_script) -> list[dict]:
    _dict_raw_script = json.loads(raw_script.contents[0])

    brands_with_id: list[dict] = _dict_raw_script["props"]["initialState"][
        "properties"
    ]["home"]["propertyMap"]["brands"]["value"][0]["brand"]["options"]

    return brands_with_id


def _get_brands_with_links(raw_script) -> list[dict]:
    _dict_raw_script = json.loads(raw_script.contents[0])

    brands_with_links: list[dict] = _dict_raw_script["props"]["initialState"][
        "home"
    ]["links"]

    return brands_with_links
