from db.dals import ModelDAL
from db.session import get_session
from parsing.models import Model


async def create_models(models: tuple[Model]):
    async with get_session() as session:
        async with session.begin():
            model_dal = ModelDAL(session)
            await model_dal.save_models(models=models)


async def clean_models():
    async with get_session() as session:
        async with session.begin():
            model_dal = ModelDAL(session)
            await model_dal.clean_models()
