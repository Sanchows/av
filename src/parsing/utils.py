import asyncio


async def gather_data(*coros_or_futures) -> tuple:
    """
    Returns parsed elements, since each of the coros returns nested
    combinations of lists/tuples
    """

    gathered = await asyncio.gather(*coros_or_futures, return_exceptions=False)
    result = tuple(item for x in gathered for item in x)

    return result
