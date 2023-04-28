import asyncio
import itertools

from actions.adverts import create_adverts
from actions.brands import clean_brands, create_brands
from actions.models import clean_models, create_models


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
    await clean_brands()
    await create_brands(brands=brands)

    models = await gather_data(
        *(get_models_by_brand(brand=brand) for brand in brands),
    )
    await clean_models()
    await create_models(models=models)

    for batched_models in batch(models, 10):
        adverts = await gather_data(
            *(get_adverts_by_model(model=model) for model in batched_models)
        )
        await create_adverts(adverts=adverts)


async def run():
    await main()


if __name__ == "__main__":
    asyncio.run(run())
