import json
from pony.orm import db_session, Required
from components.db import db, Audio

# 增加数据
@db_session
def insert_audio(title, description, url, uuid, created_at, update_at):
    new_audio = Audio(title=title, description=description, url=url, uuid=uuid, created_at=created_at, update_at=update_at)
    return;


# 删除数据
@db_session
def delete_audio_by_uuid(uuid: [str]):
    db.execute("DELETE from audio WHERE uuid=$uuid")

    return

# 更新数据
@db_session
def update_audio_by_uuid(uuid: [str], title: str):
    db.execute("UPDATE audio SET title=$title WHERE uuid=$uuid")

    return


# 查询数据
@db_session
def get_audio_list():
    rows = db.select(
        "SELECT * FROM audio"
    )
    
    print("rows=====>", rows)

