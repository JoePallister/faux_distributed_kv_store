from fastapi import FastAPI
from pydantic import BaseModel

NUM_NODES = 4


class Item(BaseModel):
    key: str
    value: str


app = FastAPI()

stores = [{} for _ in range(NUM_NODES)]


@app.get("/store")
def read_stores():
    return stores


@app.get("/store/{node_id}")
def read_store(node_id: int):
    if 0 <= node_id < NUM_NODES:
        return stores[node_id]
    return {"error": "Node not found"}


@app.post("/store")
def create_item(item: Item):
    node_id = hash(item.key) % NUM_NODES
    store = stores[node_id]
    store[item.key] = item.value
    return {"message": f"Item with key '{item.key}' created successfully."}
