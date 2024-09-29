from fastapi import APIRouter, Header
from utils.resp import resp_err, resp_ok, resp_data
from pydantic import BaseModel
import time
import base64
import openai

audio_router = APIRouter()

# 大模型生成音频以及文本
class llmSearchReq(BaseModel):
    t: str;
    l: str;
    m: str;

# 定一个字典做映射使用
model_mapping = {
    "llama3.1:405b": "llama3-1-405b",
    "qwen2:72b": "qwen2-72b",
}

# hs用于生成不同音频命名
milliseconds = str(int(time.time() * 1000))

@audio_router.post("/api/generate_audio_text")
async def ollama_model_api(req: llmSearchReq, authorization: str = Header(None)):
    """
    Generate an audio story based on the given theme and language requirements

    Args:
        req (ollamaSearchReq): A request object containing the theme and language requirements
        authorization (str, optional): Authorization header. Defaults to None.

    Returns:
        str: The text content of the generated audio story
    """
    print('req===>', req);
    description = f"讲述一则关于{req.t}的故事，要求120字左右，用词优美，随机生成不同人物主题，不同故事情节，不需要故事总结，用{req.l}输出"
    response = await generate_audio(description, model_mapping[req.m])
    return response;


async def generate_audio(description, m="llama3-1-405b"):
  client = openai.OpenAI(
    base_url=f"https://{m}.lepton.run/api/v1/",
    api_key="6XN3K2Ydd7kroaDiBE3r0a9KZJWO0suZ"
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
          "content": description
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
  with open(milliseconds + '.mp3', 'wb') as f:
    f.write(buf)
    
  data = {
    "url": milliseconds + '.mp3',
    "content": finalcontent,
  }
  
  print("\nAudio saved to output.mp3")
  print('finalcontent===>', finalcontent)

  return resp_data(data);
  
