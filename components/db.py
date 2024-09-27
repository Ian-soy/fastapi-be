import os
from supabase import create_client, Client

# 获取 Supabase 的 URL 和 API 密钥，可以从环境变量中获取或者直接在代码中设置
url = os.environ.get('SUPABASE_URL') or 'https://zfwxxuawqlcmnsbdgksq.supabase.co'
key = os.environ.get('SUPABASE_KEY') or 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpmd3h4dWF3cWxjbW5zYmRna3NxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU1NDg2MTIsImV4cCI6MjA0MTEyNDYxMn0.TQqyWfV0KMxYPZlkjwRubtdctJvCBHzuovr8lLZ5R5A'

# 创建 Supabase 客户端
db: Client = create_client(url, key)

# 例如，查询一个表中的数据
# response = supabase.table('audio').select('*').execute()
response = db.query(
  'SELECT * FROM audio'
)

data = response
print(data)