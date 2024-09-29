from components.log import log
from supabase import create_client
import os

def storage_client():
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    supabase = create_client(supabase_url, supabase_key)

    # 获取存储客户端对象
    storage = supabase.storage

    log.info("init env ok")
    
    return storage