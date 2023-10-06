import datetime
import json
import os
import pathlib

import click
from sqlalchemy.exc import IntegrityError

from .extensions import db
from .models import Article, Author, Tag, User

fixtures_folder = pathlib.Path(__file__).resolve().parent / "data" / "fixtures"
fixtures = [
    (fixtures_folder / r"tags.json", Tag),
    (fixtures_folder / r"users.json", User),
    (fixtures_folder / r"authors.json", Author),
    (fixtures_folder / r"articles.json", Article),
]


def _init_db():
    if not all(
        [db.engine.dialect.has_table(db.engine, table.__tablename__) for table in [User, Tag, Article, Author]]
    ):
        db.create_all()
        print("DB initialized.")


def _create_superuser():
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


def _create_tags():
    from blog.models import Tag

    count = 0
    for name in ["flask", "django", "python", "sqlalchemy", "news"]:
        if not Tag.query.filter_by(name=name).one_or_none():
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
            count += 1
    if count:
        print(f"Created {count} tags.")


def _load_fixtures():
    def convert_datetime(datetime_str: str):
        return datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00")).replace(microsecond=0)

    def load_fixture(fixture_path: str | pathlib.Path, model_obj: db.Model):
        count = 0
        with open(fixture_path) as file:
            data_list: dict = json.load(file)
            for data_obj in data_list:
                if "created_at" in data_obj.keys():
                    data_obj["created_at"] = convert_datetime(data_obj["created_at"])

                id_ = data_obj.pop("id")
                if db.session.query(model_obj).get(id_):
                    continue

                tags = []
                if "tags" in data_obj.keys():
                    tags = data_obj.pop("tags")

                obj = model_obj(**data_obj)
                db.session.add(obj)

                if tags:
                    selected_tags = Tag.query.filter(Tag.id.in_(tags))
                    for tag in selected_tags:
                        obj.tags.append(tag)

                try:
                    db.session.commit()
                    count += 1
                except IntegrityError:
                    db.session.rollback()
        return count

    for fixture, model in fixtures:
        loaded_count = load_fixture(fixture, model)
        if loaded_count:
            print(f'Fixture: {fixture}: loaded {loaded_count} objects."')


def initialize_db_objects():
    _init_db()
    _create_superuser()
    _create_tags()
    _load_fixtures()


@click.command("init-db")
def init_db():
    _init_db()


@click.command("create-superuser")
def create_superuser():
    _create_superuser()


@click.command("create-tags")
def create_tags():
    _create_tags()


@click.command("load-fixtures")
def load_fixtures():
    _load_fixtures()
