from fastapi import APIRouter

test_router = APIRouter()

@test_router.get("/list")
def read_list(b: str = None, a: str = None):
    return {"b": b, "a": a}

