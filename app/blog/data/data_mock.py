import datetime
import json
import pathlib

# test data created with https://www.databasetestdata.com

current_path = pathlib.Path(__file__).resolve().parent

users_fixture = current_path / r"fixtures/users.json"
articles_fixture = current_path / r"fixtures/articles.json"

USERS = {}
ARTICLES = {}


def convert_datetime(datetime_str: str):
    return datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00")).replace(microsecond=0)


for data_dict, filename in [(USERS, users_fixture), (ARTICLES, articles_fixture)]:
    with open(filename) as file:
        data_list = json.load(file)
        for data_obj in data_list:
            data_dict[data_obj["id"]] = data_obj
            created_at = data_dict[data_obj["id"]]["created_at"]
            data_dict[data_obj["id"]]["created_at"] = convert_datetime(created_at)
