import datetime
import json
import pathlib

import click

from .db import db
from .models import Article, User


@click.command("init-db")
def init_db():
    db.create_all()
    print("DB initialized.")


@click.command("load-fixtures")
def create_users():
    def convert_datetime(datetime_str: str):
        return datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00")).replace(microsecond=0)

    def load_fixture(fixture_path: str | pathlib.Path, model_obj: db.Model):
        with open(fixture_path) as file:
            data_list = json.load(file)
            for data_obj in data_list:
                data_obj["created_at"] = convert_datetime(data_obj["created_at"])
                db.session.add(model_obj(**data_obj))
            db.session.commit()

    fixtures_folder = pathlib.Path(__file__).resolve().parent / "data" / "fixtures"

    print(fixtures_folder)
    fixtures = [
        (fixtures_folder / r"users.json", User),
        (fixtures_folder / r"articles.json", Article),
    ]

    for fixture, model in fixtures:
        load_fixture(fixture, model)

    print("All fixtures loaded.")
