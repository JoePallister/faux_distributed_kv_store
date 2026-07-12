import bisect
import hashlib
from fastapi import FastAPI
from pydantic import BaseModel
import logging

NUM_NODES = 4
HASH_RING_SIZE = 2**32
NODE_NAMES = [f"node_{i}" for i in range(NUM_NODES)]
ring = [(i * (HASH_RING_SIZE // NUM_NODES), NODE_NAMES[i]) for i in range(NUM_NODES)]
stores = {NODE_NAMES[i]: {} for i in range(NUM_NODES)}

logging.basicConfig(level=logging.INFO)


def hash(key: str) -> int:
    return int(hashlib.sha256(key.encode()).hexdigest(), 16)


def find_node(key: str, hash_ring_size: int = HASH_RING_SIZE, ring: list = ring) -> str:
    hash_value = hash(key) % hash_ring_size

    positions = [p for p, node in ring]

    idx = bisect.bisect_left(positions, hash_value)

    if idx == len(ring):
        idx = 0

    return ring[idx][1]


def reassign_keys(node_name: str, ring: list, stores: dict):
    pairs_to_reassign = stores[node_name].copy()
    stores.pop(node_name)
    ring = [node for node in ring if node[1] != node_name]
    for key, value in pairs_to_reassign.items():
        new_node_name = find_node(key, HASH_RING_SIZE, ring)
        stores[new_node_name][key] = value
    return ring


class Item(BaseModel):
    key: str
    value: str


app = FastAPI()


@app.get("/store")
def read_stores():
    return stores


@app.get("/ring")
def read_ring():
    return ring


@app.get("/store/{node_name}")
def read_store(node_name: str):
    if node_name in stores:
        return stores[node_name]
    return {"error": "Node not found"}


@app.post("/store")
def create_item(item: Item):
    node_name = find_node(item.key, HASH_RING_SIZE, ring)
    store = stores[node_name]
    store[item.key] = item.value
    return {"message": f"Item with key '{item.key}' created successfully."}


@app.delete("/store/{node_name}")
def delete_node(node_name: str):
    global ring
    ring = reassign_keys(node_name, ring, stores)
    return {}
