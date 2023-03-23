from contextlib import asynccontextmanager

import httpx

import settings
from parsing import headers
from parsing.brands import Brand
from parsing.exceptions import MaxRetryError
from parsing.models import Model


@asynccontextmanager
async def get_client():
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(None, read=30),
        # timeout=httpx.Timeout(None, read=None),
    ) as client:
        yield client


def max_retry(f):
    async def wrapper(*args, **kwargs):
        retry_number = 0
        while retry_number <= settings.MAX_NUMBER_OF_RETRIES:
            try:
                result = await f(*args, **kwargs)
            except httpx.TransportError:
                retry_number += 1
                continue

            if result.status_code == 200:
                return result
            elif (
                (f.__name__ == "get_phone_number")
                and (result.status_code == 400)
                and (
                    result.json()["message"]
                    == "exception.advert.phones.can_not_show_for_non_active"
                )
            ):
                return None
            else:
                retry_number += 1
        raise MaxRetryError(
            f"The number of maximum retries ({settings.MAX_NUMBER_OF_RETRIES})"
            "is exceeded."
        )

    return wrapper


@max_retry
async def get_brands() -> httpx.Response:
    async with get_client() as client:
        return await client.get(
            url="https://av.by",
            headers=headers.headers_for_avby,
        )


@max_retry
async def get_models_by_brand(brand: Brand) -> httpx.Response:
    async with get_client() as client:
        return await client.post(
            url="https://api.av.by/offer-types/cars/filters/main/update",
            json=headers.body_for_models_by_brand(brand=brand),
            headers=headers.headers_for_api,
        )


@max_retry
async def get_generations_by_model(model: Model) -> httpx.Response:
    async with get_client() as client:
        return await client.post(
            url="https://api.av.by/offer-types/cars/filters/main/update",
            json=headers.body_for_generations_by_model(model=model),
            headers=headers.headers_for_api,
        )


@max_retry
async def get_adverts_by_model(
    model: Model, page_number: int
) -> httpx.Response:
    async with get_client() as client:
        return await client.post(
            url="https://api.av.by/offer-types/cars/filters/main/apply",
            json=headers.body_for_adverts_by_model(
                model=model, page_number=page_number
            ),
            headers=headers.headers_for_api,
        )


@max_retry
async def get_phone_number(advert_id: int) -> httpx.Response:
    async with get_client() as client:
        return await client.get(
            url=f"https://api.av.by/offers/{advert_id}/phones",
            headers=headers.headers_for_api,
        )
