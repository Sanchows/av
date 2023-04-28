from db.dals import AdvertDAL
from db.session import get_session
from parsing.adverts import Advert


async def create_adverts(adverts: tuple[Advert]):
    async with get_session() as session:
        async with session.begin():
            advert_dal = AdvertDAL(session)
            await advert_dal.save_adverts(adverts=adverts)
