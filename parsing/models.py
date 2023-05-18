from dataclasses import dataclass

from parsing import client
from parsing.brands import Brand


@dataclass
class Model:
    model_id: int  # 156
    label: str  # Cirrus
    brand_id: int


async def get_models_by_brand(brand: Brand) -> tuple[Model]:
    models = await _parse_models_by_brand(brand=brand)

    return models


async def _parse_models_by_brand(brand: Brand) -> tuple[Model]:
    response = await client.get_models_by_brand(brand=brand)

    models = response.json()["properties"][0]["value"][0][2]["options"]

    return tuple(
        Model(
            model_id=item["id"],
            label=item["label"],
            brand_id=brand.brand_id,
        )
        for item in models
    )
