import os
import pathlib

from dotenv import load_dotenv

from ..enums import EnvType

env_path = pathlib.Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", default=EnvType.production)
    FLASK_DEBUG = DEBUG = FLASK_ENV.upper() == EnvType.development
    FLASK_TESTING = TESTING = FLASK_ENV.upper() == EnvType.testing
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    FLASK_ADMIN_SWATCH = "cosmo"
    OPENAPI_URL_PREFIX = "/api/swagger"
    OPENAPI_SWAGGER_UI_PATH = "/"
    OPENAPI_SWAGGER_UI_VERSION = "3.22.0"
