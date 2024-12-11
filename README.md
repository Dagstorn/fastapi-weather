# FastAPI Тестовое задание

deployed on Vercel: https://weather-rest-api.vercel.app/

docs: https://weather-rest-api.vercel.app/docs

пример внещнего API: https://weather-rest-api.vercel.app/api/v1/weather/?city=Portland&country=US

пример все репорты из БД: https://weather-rest-api.vercel.app/api/v1/weather/reports/

## Features
- Получение текущих данных о погоде из внешнего погодного сервиса OpenWeatherMap API
- Операции CRUD для отчетов о погоде, хранящихся в базе данных.
- Поддержка аутентификации для определенных маршрутов через JWT токены.

## Project Structure
```plaintext
.
├── api
│   ├── auth.py                 # Маршруты аутентификации
│   └── weather_api.py          # Основные маршруты API для работы с погодой
├── infra
│   ├── database.py             # Управление соединением с базой данных и сессиями
│   └── weather_cache.py        # Пример кэширования при работе с внешним API
├── models                      
│   ├── location.py             # Модель данных о местоположении
│   ├── reports.py              # Модель данных отчетов о погоде
│   ├── users.py                # Модель данных пользователей
│   └── ValidationError.py      # Модель обработки исключений
├── schemas
│   ├── auth_schemas.py         # Модели Pydantic для аутентификации
│   ├── report_schemas.py       # Модели Pydantic для запросов отчетов
│   └── weather_schemas.py      # Модели Pydantic для данных о погоде
├── services
│   ├── auth_service.py         # Управление аутентификацией пользователей
│   ├── openweather_service.py  # Взаимодействие с OpenWeather API
│   └── report_service.py       # Операции CRUD для отчетов
├── venv                        # Виртуальное окружение
├── .env                        # Конфигурация окружения
├── .gitignore                  # Игнорируемые файлы для Git
├── main.py                     # Точка входа в приложение FastAPI
├── README.md                   # Документация проекта
├── requirements.txt            # Зависимости проекта
├── vercel.json                 # Конфигурация для деплоя в Vercel
└── weather.db                  # Локальная база данных SQLite
```


## Installation
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Dagstorn/fastapi-weather
   cd weather-rest-api
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Настройте базу данных:
   - Укажите строку подключения к базе данных в `infra/database.py`.

5. Запустите приложение:
   ```bash
   uvicorn main:api --reload
   ```

## Endpoints

### Base URL
`/api/v1/weather`

### Routes

1. #### Test External API
    **GET** `/`

    Получить данные о погоде для указанного местоположения.
    - **Query Parameters:**
      - `city`: Название города (обязательно)
      - `state`: Название штата (опционально, только для US)
      - `country`: Название страны (опционально, по умолчанию KZ)
      - `units`: Единицы измерения (`metric`, `imperial`) - по умолчанию: `metric`

2. #### Get All Weather Reports
    **GET** `/reports`
    Получить все сохраненные отчеты о погоде.

3. #### Add a New Report
    **POST** `/reports`
    - **Query Parameters:**
      - `city`: Название города (обязательно)
      - `state`: Название штата (опционально, только для US)
      - `country`: Название страны (опционально, по умолчанию KZ)
      - `units`: Единицы измерения (`metric`, `imperial`) - по умолчанию: `metric`

    Получает данные о погоде в указанном городе и сохроняет в базе данных с датой 
    Требуется аутентификация пользователя.

4. #### Update an Existing Report
    **PUT** `/reports/{report_id}`

    Обновить существующий отчет о погоде. Требуется аутентификация пользователя.

   - **Path Parameter:**
     - `report_id`: ID отчета для обновления

   - **Body Parameters:**
     - `city`, `state`, `country`, `units`

5. #### Delete a Report
    **DELETE** `/reports/{report_id}`

    Удалить отчет о погоде по ID. Требуется аутентификация пользователя.

   - **Path Parameter:**
     - `report_id`: ID отчета для удаления


