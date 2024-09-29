from fastapi import APIRouter, Header
from utils.resp import resp_err, resp_ok, resp_data
from pydantic import BaseModel
import requests;
import json;
import os

gpts_router = APIRouter()

# 参数验证
class SearchReq(BaseModel):
    question: str

@gpts_router.post("/gpts/search")
async def search_gpts_with_question(req: SearchReq, authorization: str = Header(None)):
    """
    Search for GPTS (Global Professional Translation Service) with the given question.

    :param req: The search request object containing the question.
    :param authorization: The authorization header containing the API key. Defaults to None.
    :return: The response containing the search results or an error message if the search fails.
    """
    indexApiKey = os.getenv("INDEX_API_KEY")
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
    url = os.getenv("KOUZI_CHAT_URL")
    data = {
      "bot_id": os.getenv("BOT_ID"),
      "conversation_id": os.getenv("CONVERSATION_ID"),
      "user": "12345",
      "query": query,
      "stream": False
    }

    # headers
    headers = {
        'Authorization': f"Bearer  {os.getenv('KOUZI_API_KEY')}",
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'api.coze.cn',
        'Connection': 'keep-alive'
    }
    # 将请求体转换为 JSON 格式的字符串
    json_data = json.dumps(data)
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)
    # 使用 json 参数自动设置正确的 Content-Type
    # 打印响应内容
    # print(response.text)
    return json.loads(response.text)
