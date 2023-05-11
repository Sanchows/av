from typing import Iterable

from db.dals import PhoneDAL
from db.session import get_session
from parsing.phones import PhoneInfo


async def create_phones(phone_info: PhoneInfo):
    async with get_session() as session:
        async with session.begin():
            phone_dal = PhoneDAL(session)
            await phone_dal.save_phones(phone_info=phone_info)


async def clean_phones():
    async with get_session() as session:
        async with session.begin():
            phone_dal = PhoneDAL(session)
            await phone_dal.clean_phones()
