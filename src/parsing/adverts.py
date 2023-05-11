from dataclasses import dataclass
from datetime import datetime

from parsing import client
from parsing.models import Model
from parsing.utils import gather_data

# from parsing.phones import Phone, get_phones


@dataclass
class Price:
    byn: int
    eur: int
    rub: int
    usd: int


@dataclass
class Photo:
    main: bool
    url: str


@dataclass
class Advert:
    advert_id: int
    status: str
    seller_name: str
    location_name: str
    short_location_name: str
    advert_type: str
    url: str
    year: int
    description: str | None
    organization_title: str | None
    published_at: datetime
    refreshed_at: datetime | None
    renewed_at: datetime | None
    #    # One-to-One
    #    price = relationship("Price", uselist=False, back_populates="advert")
    price: Price
    #    # One-to-Many
    #    photos = relationship("Photo", backref='advert')
    photos: tuple[Photo] | None
    #    videos = relationship("Video", backref='advert')
    video_url: str | None
    #    properties = relationship("Property", backref='advert')
    #    phones = relationship("Phone", backref='advert')
    # phones: tuple[Phone] | None
    brand_id: int
    model_id: int
    generation_id: int | None

    def __post_init__(self):
        """Set up published_at, published_at and renewed_at to datetime"""

        for field in ("published_at", "refreshed_at", "renewed_at"):
            value = getattr(self, field)
            if value is None or isinstance(value, datetime):
                continue
            value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
            setattr(self, field, value)


# async def get_adverts_by_generation(generation: Generation):
#     pass


def clean_duplicates(adverts: list[Advert]):
    # A sense of this function:
    # Sometimes there may be situations when the parser is working and parsing
    # page after page, and at the same time new adverts appear on the website.
    # In this case we append parsed adverts, but when we step on the next page
    # we will parse adverts again that we parsed on the previous page, because
    # adverts move through the pages depending on total of their count.
    # And there are no ideas how to control it.

    unique_ids = set({})

    for advert in adverts:
        if advert.advert_id in unique_ids:
            adverts.remove(advert)
        unique_ids.add(advert.advert_id)


async def get_adverts_by_model(model: Model) -> list[Advert]:
    pagecount_and_adverts = await _get_pagecount_and_adverts_by_model(
        model=model,
        page_number=1,
    )

    page_count, adverts = pagecount_and_adverts

    if page_count > 1:
        adverts += await gather_data(
            *(
                _parse_adverts_by_page(model=model, page_number=page_number)
                for page_number in range(2, page_count + 1)
            )
        )
    clean_duplicates(adverts=adverts)

    return adverts


async def _get_pagecount_and_adverts_by_model(
    model: Model,
    page_number: int = 1,
) -> tuple[int, list[Advert]]:
    """
    Returns `page_number` - count of pages so far, `adverts` - list[Advert]
    """

    r = await client.get_adverts_by_model(model=model, page_number=page_number)

    response = r.json()

    _adverts = response.get("adverts")

    adverts = [
        Advert(
            advert_id=item["id"],
            status=item["status"],
            seller_name=item["sellerName"],
            location_name=item["locationName"],
            short_location_name=item["shortLocationName"],
            advert_type=item["advertType"],
            url=item["publicUrl"],
            year=item["year"],
            description=item.get("description"),
            organization_title=item.get("organizationTitle"),
            published_at=item.get("publishedAt"),
            refreshed_at=item.get("refreshedAt"),
            renewed_at=item.get("renewedAt"),
            brand_id=item["metadata"]["brandId"],
            model_id=item["metadata"]["modelId"],
            generation_id=item["metadata"].get("generationId"),
            price=_get_prices(item=item),
            photos=_get_photos(item=item),
            video_url=item.get("videoUrl"),
            # phones=(
            #     await get_phones(advert_id=item["id"])
            #     if item["status"] == "active"
            #     and item["publicStatus"]["name"] == "active"
            #     else None
            # ),
            # phones=await get_phones(advert_id=item["id"])
            # phones=None
        )
        for item in _adverts
    ]

    page_count = response.get("pageCount")

    return page_count, adverts


async def _parse_adverts_by_page(
    model: Model, page_number: int
) -> list[Advert]:
    numpages_and_adverts = await _get_pagecount_and_adverts_by_model(
        model=model,
        page_number=page_number,
    )

    return numpages_and_adverts[1]


def _get_prices(item: dict) -> Price:
    _prices = item["price"]

    return Price(
        byn=_prices["byn"]["amount"],
        eur=_prices["eur"]["amount"],
        rub=_prices["rub"]["amount"],
        usd=_prices["usd"]["amount"],
    )


def _get_photos(item: dict) -> tuple | None:
    _photos = item.get("photos")

    return (
        tuple(
            Photo(
                main=photo["main"],
                url=photo["big"]["url"],
            )
            for photo in _photos
        )
        if _photos
        else None
    )
