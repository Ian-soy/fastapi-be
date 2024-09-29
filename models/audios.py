import json
from pony.orm import db_session
from components.db import db


class Gpts:
    def __init__(self, v) -> None:
        self.uuid = v["data"]["gizmo"]["id"]
        self.org_id = v["data"]["gizmo"]["organization_id"]
        self.name = v["data"]["gizmo"]["display"]["name"]
        self.description = v["data"]["gizmo"]["display"]["description"]
        self.avatar_url = v["data"]["gizmo"]["display"]["profile_picture_url"]
        self.short_url = v["data"]["gizmo"]["short_url"]
        self.author_id = v["data"]["gizmo"]["author"]["user_id"]
        self.author_name = v["data"]["gizmo"]["author"]["display_name"]
        self.created_at = v["created_at"]
        self.updated_at = v["data"]["gizmo"]["updated_at"]


# def get_gpts_from_file(file_name: str):
#     with open(file_name, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         gpts = []
#         for v in data:
#             gpt = Gpts(v)
#             print("gpts: ", gpt.name, gpt.uuid)
#             gpts.append(gpt)
            
#         return gpts


@db_session
def get_gpts_from_db(last_id: int, limit: int):
    """
    Retrieves a list of GPT records from the database.

    Args:
        last_id (int): The ID of the last retrieved record.
        limit (int): The maximum number of records to retrieve.

    Returns:
        list: A list of retrieved GPT records.

    This function queries the database for records where the ID is greater than `last_id`
    and the `index_updated_at` field is equal to 0. The records are ordered by ID in
    ascending order and limited by the specified `limit`. If `limit` is not provided or
    is less than or equal to 0, a default limit of 100 records is used.
    """
    if limit <= 0:
        limit = 100

    rows = db.select(
        "SELECT * FROM gpts WHERE id > $last_id AND index_updated_at = 0 ORDER BY id asc LIMIT $limit"
    )
    gpts = []
    for row in rows:
        gpts.append(row)

    return gpts


# @db_session
# def get_gpts_by_uuids(uuids: [str]):
#     rows = db.select(
#         "SELECT * FROM gpts WHERE uuid = ANY($uuids) ORDER BY id asc"
#     )
#     gpts = []
#     for row in rows:
#         gpts.append(row)

#     return gpts


@db_session
def update_gpts_index_time(ids: [int], index_time: int):
    db.execute("UPDATE gpts SET index_updated_at=$index_time WHERE id = ANY($ids)")

    return


@db_session
def insert_audio_index_time(ids: [int], index_time: int):
    db.execute("INSERT gpts SET index_updated_at=$index_time WHERE id = ANY($ids)")

    return



