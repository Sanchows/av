import asyncio
from datetime import datetime
import itertools
import resource

from actions.adverts import get_adverts
from actions.phones import create_phones
from parsing.phones import get_phones


def batch(iterable, size):
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
    adverts = [advert_id async for advert_id in get_adverts()]
    for batched_adverts in batch(adverts, 50):
        phones = await asyncio.gather(
            *(
                get_phones(advert_id=advert_id)
                for advert_id in batched_adverts
            ),
        )
        for phone_info in phones:
            await create_phones(phone_info=phone_info)

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
