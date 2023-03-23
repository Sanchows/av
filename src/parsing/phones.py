from dataclasses import dataclass

from parsing import client


@dataclass
class Phone:
    code: str
    number: str


async def get_phones(advert_id: int) -> tuple[Phone] | None:
    phones = await _get_phones(advert_id=advert_id)

    return phones


async def _get_phones(advert_id: int) -> tuple[Phone] | None:
    r = await client.get_phone_number(advert_id=advert_id)
    if not r:
        return None

    phones = r.json()
    return tuple(
        Phone(
            code=item["country"]["code"],
            number=item["number"],
        )
        for item in phones
    )
