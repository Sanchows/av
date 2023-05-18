from dataclasses import dataclass

from parsing import client


@dataclass
class Phone:
    code: str | None
    number: str | None


@dataclass
class PhoneInfo:
    advert_id: int
    phones: tuple[Phone] | None


async def get_phones(advert_id: int) -> PhoneInfo:
    phones = await _get_phones(advert_id=advert_id)

    return PhoneInfo(advert_id=advert_id, phones=phones)


async def _get_phones(advert_id: int) -> tuple[Phone] | None:
    r = await client.get_phone_number(advert_id=advert_id)
    if not r:
        return None

    return tuple(
        Phone(
            code=item["country"]["code"],
            number=item["number"],
        )
        for item in r.json()
    )
