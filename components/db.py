from pony.orm import Database, set_sql_debug
import os
from components.log import log
from urllib.parse import urlparse

db = Database()

def init_db():
    """
    Initializes the database connection and performs necessary configurations.

    This function sets up the database connection using the provided environment variables.
    It binds the database provider, host, user, password, and database name.
    Additionally, it generates the mapping for the database tables and enables SQL debugging.
    Finally, it logs the successful initialization of the database.

    Note:
    - The function assumes that the necessary environment variables for the database connection are set.

    Returns:
        None
    """
    database_url = os.getenv("DATABASE_URL")
    url = urlparse(database_url)

    db.bind(
        provider=url.scheme,
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:]
    )
    db.generate_mapping(create_tables=True)

    set_sql_debug(True)

    print("init db ok")





# import os
# from supabase import create_client, Client

# # 获取 Supabase 的 URL 和 API 密钥，可以从环境变量中获取或者直接在代码中设置
# url = os.environ.get('SUPABASE_URL') or 'https://zfwxxuawqlcmnsbdgksq.supabase.co'
# key = os.environ.get('SUPABASE_KEY') or 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpmd3h4dWF3cWxjbW5zYmRna3NxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU1NDg2MTIsImV4cCI6MjA0MTEyNDYxMn0.TQqyWfV0KMxYPZlkjwRubtdctJvCBHzuovr8lLZ5R5A'

# # 创建 Supabase 客户端
# db: Client = create_client(url, key)

# # 例如，查询一个表中的数据
# response = db.table('audio').select('*').execute()
# # response = db.query(
# #   'SELECT * FROM audio'
# # )

# data = response
# print(data)
