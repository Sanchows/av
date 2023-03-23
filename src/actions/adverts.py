from db.dals import AdvertDAL
from parsing.adverts import Advert


async def _create_adverts(adverts: tuple[Advert], session):
    async with session.begin():
        advert_dal = AdvertDAL(session)
        await advert_dal.save_adverts(adverts=adverts)
