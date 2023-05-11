from typing import Iterable

from db.dals import PhoneDAL
from db.session import get_session
from parsing.phones import Phone


async def create_phones(phones: Iterable[Phone]):
    async with get_session() as session:
        async with session.begin():
            phone_dal = PhoneDAL(session)
            await phone_dal.save_phones(phones=phones)


async def clean_phones():
    async with get_session() as session:
        async with session.begin():
            phone_dal = PhoneDAL(session)
            await phone_dal.clean_phones()
