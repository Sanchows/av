import asyncio
from datetime import datetime
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
    start = datetime.now()

    brands = await get_brands()

    async with get_db() as db:
        await _clean_brands(db)

    async with get_db() as db:
        await _create_brands(brands=brands, session=db)

    models = await gather_data(
        *(get_models_by_brand(brand=brand) for brand in brands),
    )

    adverts = await gather_data(
        *(get_adverts_by_model(model=model) for model in models)
    )

    start_saving = datetime.now()

    # I caught an exception "the number of query arguments cannot exceed 32767"
    # therefore, we will record 5000 pieces each:
    MAX_SIZE_OF_ADVERTS_FOR_UPSERT = 5000
    batched_adverts = tuple(batch(adverts, MAX_SIZE_OF_ADVERTS_FOR_UPSERT))
    try:
        for ads in batched_adverts:
            async with get_db() as db:
                await _create_adverts(adverts=ads, session=db)
    except Exception as e:
        print(str(e)[:2000])
        import sys
        sys.exit()

    finish_saving = datetime.now()
    finish = datetime.now()
    print(finish - start)
    print(finish_saving - start_saving)


async def run():
    await main()


if __name__ == "__main__":
    asyncio.run(run())
