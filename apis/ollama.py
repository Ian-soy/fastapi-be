from fastapi import APIRouter, Header
from pydantic import BaseModel
import requests;

ollama_router = APIRouter()

class ollamaSearchReq(BaseModel):
    m: str;
    q: str;
    s: bool;

# ollama 模型api请求
@ollama_router.post("/ollama/api/generate")
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
