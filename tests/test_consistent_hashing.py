from app_consistent_hashing import (
    find_node,
    reassign_keys_and_delete_node,
    construct_hash_ring,
    store_item,
    Item,
    hash,
)


def find_node_name_naive(key: str, hash_ring_size: int, ring: list) -> int:
    hash_value = hash(key) % hash_ring_size
    while hash_value not in [p for p, _ in ring]:
        hash_value = (hash_value + 1) % hash_ring_size

    return next(node for p, node in ring if p == hash_value)


def test_find_node():
    test_key = "test_key"
    hash_ring_size = 9
    num_nodes = 3
    node_names = [f"node_{i}" for i in range(num_nodes)]
    test_ring = construct_hash_ring(node_names, hash_ring_size)
    test_stores = {node_name: {} for node_name in node_names}
    store_item(
        Item(key=test_key, value="test_value"), stores=test_stores, ring=test_ring
    )
    expected_node = find_node_name_naive(test_key, hash_ring_size, test_ring)
    assert find_node(test_key, hash_ring_size, test_ring) == expected_node


def test_find_node_wrap_around():
    test_key = "test_key_1"
    hash_ring_size = 9
    test_ring = [(0, "node1"), (3, "node2"), (6, "node3")]
    print(f"Hash for {test_key}: {hash(test_key) % hash_ring_size}")
    # Hash gives 8 for this key, so it should map to node1
    assert find_node(test_key, hash_ring_size, test_ring) == "node1"


def test_reassign_keys():
    test_stores = {
        "node1": {"key1": "value1"},
        "node2": {"key2": "value2"},
        "node3": {"key3": "value3"},
    }
    test_ring = [(0, "node1"), (3, "node2"), (6, "node3")]
    new_ring = reassign_keys_and_delete_node("node2", test_ring, test_stores)

    # After removing node2, it should not be in the new ring
    assert all(node[1] != "node2" for node in new_ring)

    # The key from node2 should be reassigned to either node1 or node3
    reassigned_node = find_node("key2", 9, new_ring)
    assert reassigned_node in ["node1", "node3"]
    assert "key2" in test_stores[reassigned_node]

    # The other keys should remain in their original nodes
    assert "key1" in test_stores["node1"]
    assert "key3" in test_stores["node3"]
