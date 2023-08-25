import datetime
import json
import os
import pathlib

import click
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from .extensions import db
from .models import Article, Author, Tag, User


@click.command("init-db")
def init_db():
    db.create_all()
    print("DB initialized.")


@click.command("create-superuser")
def create_superuser():
    username = os.getenv("SUPERUSER_LOGIN")
    user_data = {
        "username": username,
        "password": os.getenv("SUPERUSER_PASSWORD"),
        "email": os.getenv("SUPERUSER_EMAIL"),
        "fullname": username,
        "is_staff": True,
    }
    if not User.query.filter_by(username=username).one_or_none():
        db.session.add(User(**user_data))
        db.session.commit()
        print(f'Superuser "{username}" initialized.')
    else:
        print(f'Superuser "{username}" already exists.')


@click.command("load-fixtures")
def create_users():
    def convert_datetime(datetime_str: str):
        return datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00")).replace(microsecond=0)

    def load_fixture(fixture_path: str | pathlib.Path, model_dict_obj: db.Model):
        print(f'Loading fixture "{fixture}"...', end=" ")
        counter = 0
        with open(fixture_path) as file:
            data_list = json.load(file)
            for data_obj in data_list:
                if "created_at" in data_obj.keys():
                    data_obj["created_at"] = convert_datetime(data_obj["created_at"])
                tags = []
                if "tags" in data_obj.keys():
                    tags = data_obj.pop("tags")

                model_obj = model_dict_obj(**data_obj)
                db.session.add(model_obj)

                if tags:
                    selected_tags = Tag.query.filter(Tag.id.in_(tags))
                    for tag in selected_tags:
                        model_obj.tags.append(tag)

                try:
                    db.session.commit()
                    counter += 1
                except (IntegrityError, PendingRollbackError):
                    db.session.rollback()
        return counter

    fixtures_folder = pathlib.Path(__file__).resolve().parent / "data" / "fixtures"

    fixtures = [
        (fixtures_folder / r"tags.json", Tag),
        (fixtures_folder / r"users.json", User),
        (fixtures_folder / r"authors.json", Author),
        (fixtures_folder / r"articles.json", Article),
    ]

    for fixture, model in fixtures:
        loaded_count = load_fixture(fixture, model)
        print(f'loaded {loaded_count} objects."')


@click.command("create-tags")
def create_tags():
    from blog.models import Tag

    counter = 0
    for name in ["flask", "django", "python", "sqlalchemy", "news"]:
        try:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
            counter += 1
        except (IntegrityError, PendingRollbackError) as ex:
            print(ex)
    print("Tags created")
