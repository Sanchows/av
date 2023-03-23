from db.dals import BrandDAL
from parsing.brands import Brand


async def _clean_brands(session):
    async with session.begin():
        brand_dal = BrandDAL(session)
        await brand_dal.clean_brands()


async def _create_brands(brands: tuple[Brand], session):
    async with session.begin():
        brand_dal = BrandDAL(session)
        await brand_dal.save_brands(brands=brands)
