from dataclasses import dataclass

from parsing import client
from parsing.models import Model


@dataclass
class Generation:
    generation_id: int  # 4748
    label: str  # B5
    year_from: int  # 1996
    year_to: int | None  # 2000
    model_id: int  # 5912


async def get_generations_by_model(model: Model) -> tuple[Generation]:
    generations = await _parse_generations_by_model(model=model)

    return generations


async def _parse_generations_by_model(model: Model) -> tuple[Generation]:
    response = await client.get_generations_by_model(model=model)

    generations = response.json()["properties"][0]["value"][0][3]["options"]

    return tuple(
        Generation(
            generation_id=item["id"],
            label=item["label"],
            year_from=item["metadata"]["yearFrom"],
            year_to=item["metadata"].get("yearTo"),
            model_id=model.model_id,
        )
        for item in generations
    )
