from fastapi import APIRouter, Header
from utils.resp import resp_err, resp_ok, resp_data
from pydantic import BaseModel
from service.generate import generate_audio

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

    description = f"讲述一则关于{req.t}的故事，要求120字左右，用词优美，随机生成不同人物主题，不同故事情节，不需要故事总结，用{req.l}输出"
    response = await generate_audio(description, model_mapping[req.m], req.t)
    
    print('response==ollama_model_api=====>', response.json());
    return resp_data(response.json());
