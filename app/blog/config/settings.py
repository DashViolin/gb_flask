import os
import pathlib

from dotenv import load_dotenv

from ..enums import EnvType

env_path = pathlib.Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", default=EnvType.production)
    DEBUG = FLASK_ENV.upper() == EnvType.development
    TESTING = FLASK_ENV.upper() == EnvType.testing
    FLASK_DEBUG = DEBUG
    FLASK_TESTING = TESTING
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
