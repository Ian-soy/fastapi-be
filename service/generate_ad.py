from models.audios import insert_audio
from components.spb import storage_client
from components.log import log
from service.generate_img import generate_image
import time
import base64
import openai
import os
import uuid
import datetime

current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
current_timestamp = str(int(datetime.datetime.now().timestamp()) * 1000 )
# 生成一个随机的 UUID
random_uuid = str(uuid.uuid4())

# 生成音频文件
async def generate_audio(des, m="llama3-1-405b", title=''):
  client = openai.OpenAI(
    base_url=f"https://{m}.lepton.run/api/v1/",
    api_key=os.getenv("LEPTON_API_KEY")
  )
  
  # calls the api
  completion = client.chat.completions.create(
    model=m,
    # This specifies what audio input and output should be
    extra_body={
      # output formats
      "require_audio": True,
      "tts_preset_id": "lily",
    },
    # this gets you audio input
    messages=[
        {
          "role": "user", 
          "content": des
        }
    ],
    max_tokens=600,
    stream=True,
  )

  # Get both text and audios
  audios = []
  finalcontent = ""
  for chunk in completion:
    if not chunk.choices:
      continue
    content = chunk.choices[0].delta.content
    audio = getattr(chunk.choices[0], 'audio', [])
    if content:
      finalcontent += content
    if audio:
      audios.extend(audio)

  buf = b''.join([base64.b64decode(audio) for audio in audios[:]])
  with open(random_uuid + '.mp3', 'wb') as f:
    f.write(buf)
  
  response = await save_to_bucket(finalcontent, title)

  return response;
  
# 上传到bucket、数据库、并删除本地文件
async def save_to_bucket(description, title):

  SUPABASE_URL = os.getenv("SUPABASE_URL")
  SUPABASE_STORAGE_URL = os.getenv("SUPABASE_STORAGE_URL")
  prefix_url = SUPABASE_URL + '' + SUPABASE_STORAGE_URL
  # 背景图片地址
  img_url = await get_image(description)

  # 读取 MP3 文件内容
  with open(random_uuid + '.mp3', 'rb') as file:
    mp3_content = file.read()

  bucket_name = 'resource-online'
  file_name = "/file/" + current_timestamp + '/' + random_uuid + '.mp3'

  response = storage_client().from_(bucket_name).upload(file_name, mp3_content, {
    'content-type': 'audio/mpeg',
  })
  
  # 插入数据库
  insert_audio(title, description, prefix_url + file_name, prefix_url + img_url, random_uuid, current_time, current_time)
  
  # 上传完成之后删除本地文件
  os.remove(random_uuid + '.mp3')
  
  return response;


# 生成图片
async def get_image(des):
  url = generate_image(des, random_uuid, current_timestamp)
  return url

