from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    key: str
    value: str


app = FastAPI()

store = {}


@app.get("/store")
def read_store():
    return store


@app.post("/store")
def create_item(item: Item):
    store[item.key] = item.value
    return {"message": f"Item with key '{item.key}' created successfully."}
