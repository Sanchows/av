import asyncio
import itertools

from actions.adverts import _create_adverts
from actions.brands import _clean_brands, _create_brands
from db.session import get_db
from parsing.adverts import get_adverts_by_model
from parsing.brands import get_brands
from parsing.models import get_models_by_brand
from parsing.utils import gather_data


def batch(iterable, size):
    # Starting with Python 3.12, this exact implementation
    # is available as itertools.batched

    it = iter(iterable)
    while item := tuple(itertools.islice(it, size)):
        yield item


async def main():
    brands = await get_brands()

    async with get_db() as db:
        await _clean_brands(db)

    async with get_db() as db:
        await _create_brands(brands=brands, session=db)

    models = await gather_data(
        *(get_models_by_brand(brand=brand) for brand in brands),
    )

    for batched_models in batch(models, 10):
        adverts = await gather_data(
            *(get_adverts_by_model(model=model) for model in batched_models)
        )
        async with get_db() as db:
            await _create_adverts(adverts=adverts, session=db)


async def run():
    await main()


if __name__ == "__main__":
    asyncio.run(run())
