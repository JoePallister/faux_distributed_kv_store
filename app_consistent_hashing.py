import bisect
import hashlib
from fastapi import FastAPI
from pydantic import BaseModel
import logging

NUM_NODES = 4
HASH_RING_SIZE = 2**32
NODE_NAMES = [f"node_{i}" for i in range(NUM_NODES)]

logging.basicConfig(level=logging.INFO)


class Item(BaseModel):
    key: str
    value: str


def hash(key: str) -> int:
    return int(hashlib.sha256(key.encode()).hexdigest(), 16)


def construct_hash_ring(
    node_names: list,
    hash_ring_size: int = HASH_RING_SIZE,
) -> list:
    return sorted(
        (hash(node_name) % hash_ring_size, node_name) for node_name in node_names
    )


ring = construct_hash_ring(NODE_NAMES, HASH_RING_SIZE)


def construct_stores(ring: list) -> dict:
    return {node_name: {} for _, node_name in ring}


stores = construct_stores(ring)


def find_node(key: str, hash_ring_size: int = HASH_RING_SIZE, ring: list = ring) -> str:
    hash_value = hash(key) % hash_ring_size

    positions = [p for p, node in ring]

    idx = bisect.bisect_left(positions, hash_value)

    if idx == len(ring):
        idx = 0
    return ring[idx][1]


def store_item(
    item: Item, stores: dict, ring: list, hash_ring_size: int = HASH_RING_SIZE
):
    node_name = find_node(item.key, hash_ring_size=hash_ring_size, ring=ring)
    stores[node_name][item.key] = item.value
    logging.info(f"Stored key '{item.key}' in node '{node_name}'.")


def reassign_keys_and_delete_node(node_name: str, ring: list, stores: dict):
    pairs_to_reassign = stores[node_name].copy()
    stores.pop(node_name)
    ring = [node for node in ring if node[1] != node_name]
    for key, value in pairs_to_reassign.items():
        new_node_name = find_node(key, hash_ring_size=HASH_RING_SIZE, ring=ring)
        stores[new_node_name][key] = value
    return ring


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
    store_item(item, stores, ring)
    return {"message": f"Item with key '{item.key}' created successfully."}


@app.delete("/ring/{node_name}")
def delete_node(node_name: str):
    global ring
    ring = reassign_keys_and_delete_node(node_name, ring, stores)
    return ring


# @app.post("/ring/{node_name}")
# def add_node(node_name: str):
#     global ring
#     ring = add_node_and_reassign_keys(node_name, ring, stores)
#     return ring
