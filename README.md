# av
- Работа приложения основана на открытом API сервиса, который доступен каждому без аутентификации.
- Приложение разрабатывается в ознакомительных с программированием и технологиями целях.

# TODO
- выборка объявлений по конкретным поколениям модели (по определенным годам выпуска)
- выборка объявлений по всевозможным критериям, таким как: тип двигателя, наличие ABS, цвет и т.д.
- уведомление о новых объявлениях конкретной модели или поколения
- выявление "перекупов" путём наличия одинаковых мобильных номеров в разных объявлениях. Ставить красный флаг, когда при этом еще и указаны разные имена
- реализация Telegram бота для взаимодействия
- fastapi для реализации API
- возможно реализация кэша для снижения нагрузки на бд.
- защита от троттлинга API эндпоинтов
- продумать в какое время запускать сбор всех объявлений, обновление мобильных телефонов и тд.

# interface / What can it do?
- Выборка всех объявлений с сайта за 3-4 минуты (более 57000 штук)
- Выборка списка брендов с сайта (BMW, Mercedes, Alfa Romeo и т.д.)
- Выборка моделей конкретного бренда (для Audi это A3, A4, A5, A6 и т.д.)
- Выборка номера мобильного телефона с объявления
- Работа с БД

# features
- Полностью асинхронный код (asyncpg, HTTPX, SQLAlchemy[asyncio])
- Оптимизировано по скорости сохранение в БД большого количества записей за один запрос.
- Продуман момент, когда в БД уже имеются найденные объявления на сайте. Если на сайте другое то только тогда обновить запись в БД конкретным способом. Всё работает за ровно 1 запрос к БД.

# small ram usage
- Несмотря на работу с немалым объемом информации (порядка 57000 больших JSON-объектов), приложение в пике занимает не больше 300 МБ (настраивается)
- Оптимизирована по памяти работа с БД.
- Доступна регулировка баланса производительностью и оптимизацией ресурсов сервера (выше скорость - больше ресурсов сервера)

# stack
- Python3.10
- HTTPX
- SQLAlchemy 2.0 [async]
- Alembic
- TODO: fastapi, aiogram
