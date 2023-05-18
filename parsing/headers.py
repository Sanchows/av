import fake_useragent

from parsing.brands import Brand
from parsing.models import Model
import settings


location = settings.BASE_DIR / f"fake_useragent{fake_useragent.VERSION}.json"

ua = fake_useragent.UserAgent(
    use_external_data=True, cache_path=location.as_posix()
)
# ua.update()


def body_for_models_by_brand(brand: Brand):
    return {
        "properties": [
            {
                "modified": True,
                "name": "brands",
                "value": [
                    [
                        {"name": "brand", "value": brand.brand_id},
                    ]
                ],
            }
        ]
    }


def body_for_generations_by_model(model: Model):
    return {
        "properties": [
            {
                "modified": True,
                "name": "brands",
                "value": [
                    [
                        {"name": "brand", "value": model.brand_id},
                        {"name": "model", "value": model.model_id},
                    ]
                ],
            }
        ]
    }


def body_for_adverts_by_model(model: Model, page_number: int):
    return {
        "page": page_number,
        "properties": [
            {
                "name": "brands",
                "value": [
                    [
                        {"name": "brand", "value": model.brand_id},
                        {"name": "model", "value": model.model_id},
                    ]
                ],
            },
        ],
    }


headers_for_api = {
    "Content-Type": "application/json",
    "User-Agent": ua.random,
    "x-device-type": "web.desktop",
}


headers_for_avby = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/"
    #           "avif,image/webp,image/apng,*/*;q=0.8,application/signed-excha"
    #           "nge;v=b3;q=0.9",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    # "Cache-Control": "max-age=0",
    # "Connection": "keep-alive",
    # "Host": "av.by",
    # "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";'
    #              'v="92"',
    # "sec-ch-ua-mobile": "?0",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "none",
    # "Sec-Fetch-User": "?1",
    # "Upgrade-Insecure-Requests": "1",
    "User-Agent": ua.random,
}
