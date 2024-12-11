import os
import fastapi
import uvicorn
from api import weather_api, auth
from infra.database import Base, engine
from services import openweather_service, auth_service
from dotenv import load_dotenv

api = fastapi.FastAPI()

def configure():
    load_dotenv()
    configure_apikeys()
    configure_jwt()

    api.include_router(weather_api.router)
    api.include_router(auth.router)

    Base.metadata.create_all(bind=engine)


def configure_apikeys():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise Exception("Openweather API_KEY is not set. Please configure it in the environment.")
    openweather_service.API_KEY = api_key


def configure_jwt():
    jwt_key = os.getenv("JWT_SECRET")
    if not jwt_key:
        raise Exception("JWT_SECRET is not set. Please configure it in the environment.")
    auth_service.JWT_SECRET = jwt_key


if __name__ == "__main__":
    configure()
    uvicorn.run(api, port=8000, host="0.0.0.0", reload=True)
else:
    configure()