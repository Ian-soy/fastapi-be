from fastapi import FastAPI, Header
import requests;
import json;
import os;
from utils.resp import resp_err, resp_ok, resp_data
from pydantic import BaseModel
from typing import Optional
import time

# 示例化
app = FastAPI()
# headers
headers = {
    'Authorization': 'Bearer pat_IoDJ0YSNeNU1GVMlDErUPzejSNENL7h338UM9VlXZSci63bkerbMDzV5VWVQJRT0',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Host': 'api.coze.cn',
    'Connection': 'keep-alive'
}

# 参数验证
class SearchReq(BaseModel):
    question: str

@app.post("/gpts/search")
async def search_gpts_with_question(req: SearchReq, authorization: str = Header(None)):
    """
    Search for GPTS (Global Professional Translation Service) with the given question.

    :param req: The search request object containing the question.
    :param authorization: The authorization header containing the API key. Defaults to None.
    :return: The response containing the search results or an error message if the search fails.
    """
    indexApiKey = "gsk-pyj"
    authApiKey = ""
    if authorization:
        authApiKey = authorization.replace("Bearer ", "")
    if authApiKey != indexApiKey:
        return resp_err("Access Denied")

    if req.question == "":
        return resp_err("invalid params")

    try:
        gpts = search_gpts(req.question)

        return resp_data(gpts)
    except Exception as e:
        return resp_err(e)



def search_gpts(query: str):
    """
    Search for GPTS with the given query.

    This function sends a POST request to the specified URL with the provided query,
    and returns the response data in JSON format.

    Args:
        query (str): The question to be searched for.

    Returns:
        dict: A dictionary containing the response data from the GPTS search.

    Raises:
        requests.exceptions.RequestException: If an error occurs while sending the request.

    Example:
        To search for GPTS with the question "What is the meaning of life?", you can call this function as follows:
        >>> result = search_gpts("What is the meaning of life?")
        >>> print(result)
        {'response': 'The meaning of life is a philosophical question...'}
    """
    url = 'https://api.coze.cn/open_api/v2/chat'
    data = {
      "bot_id": "7410284217026330624",
      "conversation_id": "7414118684790095883",
      "user": "12345",
      "query": query,
      "stream": False
    }
    # 将请求体转换为 JSON 格式的字符串
    json_data = json.dumps(data)
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)
    # 使用 json 参数自动设置正确的 Content-Type
    # 打印响应内容
    # print(response.text)
    return json.loads(response.text)

@app.get("/list")
def read_list(b: str = None, a: str = None):
    return {"b": b, "a": a}


class ollamaSearchReq(BaseModel):
    m: str;
    q: str;
    s: bool;

# ollama 模型api请求
@app.post("/ollama/api/generate")
async def ollama_model_api(req: ollamaSearchReq, authorization: str = Header(None)):
    """
    调用ollama模型api
    :param model: 模型名称
    :param prompt: 输入的prompt
    :return: 返回的结果
    """
    url = "http://127.0.0.1:11434/api/generate"
    data = {
        "model": req.m,
        "prompt": req.q,
        "stream": req.s
    }
    response = await requests.post(url, json=data)
    return response.text



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

@app.post("/api/generate_audio_text")
async def ollama_model_api(req: llmSearchReq, authorization: str = Header(None)):
    """
    Generate an audio story based on the given theme and language requirements

    Args:
        req (ollamaSearchReq): A request object containing the theme and language requirements
        authorization (str, optional): Authorization header. Defaults to None.

    Returns:
        str: The text content of the generated audio story
    """

    lan = req.l | '英语';
    description = f"讲述一则关于{req.t}故事，要求120字左右，用词优美，随机生成不同人物主题，不同故事情节，不需要故事总结，用{lan}输出"
    response = await generate_audio(description, model_mapping[req.m])
    return response;


async def generate_audio(description, m="llama3-1-405b"):
  client = openai.OpenAI(
    base_url=f"https://{m}.lepton.run/api/v1/",
    api_key="6XN3K2Ydd7kroaDiBE3r0a9KZJWO0suZ"
  )
  
  # calls the api
  completion = client.chat.completions.create(
    model="llama3-1-405b",
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

  return data;
  
