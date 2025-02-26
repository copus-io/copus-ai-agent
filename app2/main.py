from fastapi import FastAPI

from app2.bean.bean import TestRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/recommendations")
async def get_recommendations(user_id: int):
    if user_id == 1:
        return {"recommendations": ["aba", "ba"]}
    else:
        return {"recommendations": ["ab2222222a", "b2222222a"]}


@app.post("/recommendations2")
async def get_recommendations2(req : TestRequest):
    if req.user_id == 2:
        return {"recommendations": ["aba", "ba"]}
    else:
        return {"recommendations": ["ab2222222a", "b2222222a"]}
