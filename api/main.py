from fastapi import FastAPI

from .src.gen_join_link import generate_join_link

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Glory to Ukraine!"}


@app.get("/new_join/{user_id}/{address}")
async def say_hello(user_id: int, address: str):
    res = await generate_join_link(user_id, address)
    return {"invite_link": res}
