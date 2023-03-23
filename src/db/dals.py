import datetime

from sqlalchemy import and_, delete, or_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db import tables
from parsing.adverts import Advert
from parsing.brands import Brand


class AdvertDAL:
    """Data Access Layer for operating advert info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def clean_adverts(self):
        await self.db_session.execute(delete(tables.Advert))

    async def save_adverts(self, adverts: tuple[Advert]):
        adverts_for_insert = tuple(
            dict(
                advert_id=advert.advert_id,
                url=advert.url,
                description=advert.description,
                refreshed_at=advert.refreshed_at,
                published_at=advert.published_at,
                updated_at=datetime.datetime.utcnow(),
            )
            for advert in adverts
        )

        query = insert(tables.Advert).values(adverts_for_insert)

        # We shouldn't update the datetime of saved data in the database
        # and the primary key field
        data_for_update = {
            c.name: c
            for c in query.excluded
            if not c.primary_key and c.name != "saved_at"
        }

        # The data will be inserted if the advert doesn't exist yet.
        # The data will be updated if the advert (`advert_id`) already exists
        # and at least one of these statements is True:
        # 1. advert_in_db.refreshed_at < current_advert.refreshed_at
        # 2. advert_in_db.refreshed_at is None
        # and current_advert.refreshed_at isn't None
        query = query.on_conflict_do_update(
            index_elements=[tables.Advert.advert_id],
            set_=data_for_update,
            where=or_(
                tables.Advert.refreshed_at < data_for_update["refreshed_at"],
                and_(
                    tables.Advert.refreshed_at.is_(None),
                    data_for_update["refreshed_at"].isnot(None),
                ),
            ),
        )
        await self.db_session.execute(query)


class BrandDAL:
    """Data Access Layer for operating brand info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def clean_brands(self):
        await self.db_session.execute(delete(tables.Brand))

    async def save_brands(self, brands: tuple[Brand]):
        self.db_session.add_all(
            tables.Brand(
                brand_id=brand.brand_id,
                url=brand.url,
                label=brand.label,
                count=brand.count,
            )
            for brand in brands
        )
