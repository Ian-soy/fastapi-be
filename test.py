from pony.orm import db_session
from components.db import init_db
from components.db import db
init_db();

@db_session
def get_audio_list():
    rows = db.select(
        "SELECT * FROM audio"
    )
    
    print("rows=====>", rows)
  
get_audio_list();