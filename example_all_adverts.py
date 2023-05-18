import asyncio
from datetime import datetime
import itertools
import resource
from typing import Generator, Iterable, TypeVar

from actions.adverts import create_adverts
from actions.brands import clean_brands, create_brands
from actions.models import clean_models, create_models
from parsing.adverts import get_adverts_by_model
from parsing.brands import get_brands
from parsing.models import get_models_by_brand
from parsing.utils import _gather_data


T = TypeVar("T")


def batch(iterable: Iterable[T], size: int) -> Generator[tuple[T], None, None]:
    """
    Chunks an iterable object to the items.

    `batch((3, 4, 5, 6, 7, 8), 4)`
    it will return: `((3, 4, 5, 6), (7, 8))`
    """
    # Starting with Python 3.12, this exact implementation
    # is available as itertools.batched

    it = iter(iterable)
    while item := tuple(itertools.islice(it, size)):
        yield item


async def main():
    start = datetime.now()
    # print("Очищаем объявления из бд")
    # await clean_adverts()
    print("Очищаем модели из бд")
    await clean_models()
    print("Очищаем брэнды из бд")
    await clean_brands()

    print("Собираем брэнды")
    brands = await get_brands()
    print("Сохраняем брэнды в бд")
    await create_brands(brands=brands)

    print("Собираем модели")
    models = await _gather_data(
        *(get_models_by_brand(brand=brand) for brand in brands),
    )
    print("Сохраняем модели в бд")
    await create_models(models=models)

    len_models = len(models)
    remaining = len_models
    for batched_models in batch(models, 20):
        print(
            f"Собираем объявления, еще осталось собрать объявления "
            f"с {remaining} моделей. Всего {len_models} моделей"
        )
        adverts = await _gather_data(
            *(get_adverts_by_model(model=model) for model in batched_models)
        )
        print(f"Сохраняем объявления ({len(adverts)} шт.) в бд")
        await create_adverts(adverts=adverts)
        remaining -= len(batched_models)

    finish = datetime.now()
    print(f"{finish-start}")

    print(
        f"Peak memory usage: "
        f"{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024} MB"
    )


async def run():
    await main()


if __name__ == "__main__":
    asyncio.run(run())
