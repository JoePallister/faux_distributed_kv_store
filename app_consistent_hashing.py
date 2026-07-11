from fastapi import FastAPI
from pydantic import BaseModel
import logging

NUM_NODES = 4
HASH_RING_SIZE = 2**32
NODE_POSITIONS = [i * (HASH_RING_SIZE // NUM_NODES) for i in range(NUM_NODES)]

logging.basicConfig(level=logging.INFO)


def find_node(key: str) -> int:
    hash_value = hash(key) % HASH_RING_SIZE

    distances = {pos: (pos - hash_value) % HASH_RING_SIZE for pos in NODE_POSITIONS}

    closest_node_position = min(distances, key=distances.get)

    return NODE_POSITIONS.index(closest_node_position)


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
    node_id = find_node(item.key)
    store = stores[node_id]
    store[item.key] = item.value
    return {"message": f"Item with key '{item.key}' created successfully."}


@app.delete("/store/{node_id}")
def delete_node(node_id: int):
    return {}
