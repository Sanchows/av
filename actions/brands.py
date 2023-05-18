from db.dals import BrandDAL
from db.session import get_session
from parsing.brands import Brand


async def create_brands(brands: tuple[Brand]):
    async with get_session() as session:
        async with session.begin():
            brand_dal = BrandDAL(session)
            await brand_dal.save_brands(brands=brands)


async def clean_brands():
    async with get_session() as session:
        async with session.begin():
            brand_dal = BrandDAL(session)
            await brand_dal.clean_brands()
