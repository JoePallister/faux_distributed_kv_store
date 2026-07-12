from app_consistent_hashing import (
    add_node_and_reassign_keys,
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
    test_keys = ["test_key_1", "test_key_2", "test_key_3"]
    hash_ring_size = 9
    num_nodes = 3
    node_names = [f"node_{i}" for i in range(num_nodes)]
    test_ring = construct_hash_ring(node_names, hash_ring_size)
    test_stores = {node_name: {} for node_name in node_names}

    for key in test_keys:
        store_item(
            Item(key=key, value="test_value"),
            stores=test_stores,
            ring=test_ring,
            hash_ring_size=hash_ring_size,
        )
        expected_node = find_node_name_naive(key, hash_ring_size, test_ring)
        assert find_node(key, hash_ring_size, test_ring) == expected_node


def test_reassign_keys_and_delete_node():
    test_stores = {
        "node1": {"key1": "value1"},
        "node2": {"key2": "value2"},
        "node3": {"key3": "value3"},
    }
    test_ring = [(0, "node1"), (3, "node2"), (6, "node3")]
    new_ring = reassign_keys_and_delete_node(
        "node2", test_ring, test_stores, hash_ring_size=9
    )

    # After removing node2, it should not be in the new ring
    assert all(node[1] != "node2" for node in new_ring)

    # The key from node2 should be reassigned to either node1 or node3
    reassigned_node = find_node("key2", 9, new_ring)
    assert reassigned_node in ["node1", "node3"]
    assert "key2" in test_stores[reassigned_node]

    # The other keys should remain in their original nodes
    assert "key1" in test_stores["node1"]
    assert "key3" in test_stores["node3"]


def test_add_node_and_reassign_keys():
    test_keys = [
        "a",  # hash value 7
        "b",  # hash value 8
        "c",  # hash value 1
        "8",  # hash value 4
        "1",  # hash value 3
        "19",  # hash value 2
    ]
    for key in test_keys:
        print(hash(key) % 9)
    hash_ring_size = 9
    num_nodes = 3
    node_names = [f"node_{i + 1}" for i in range(num_nodes)]
    # Hashes to 8, 2, 4 respectively, so the ring will be [(2, 'node_2'), (4, 'node_3'), (8, 'node_1')]
    test_ring = construct_hash_ring(node_names, hash_ring_size)
    test_stores = {node_name: {} for node_name in node_names}
    for key in test_keys:
        store_item(
            Item(key=key, value="test_value"),
            stores=test_stores,
            ring=test_ring,
            hash_ring_size=hash_ring_size,
        )
    new_ring = add_node_and_reassign_keys(
        "node_4", test_ring, test_stores, hash_ring_size=hash_ring_size
    )
    # Hashes to 3 so the ring will be [(2, 'node_2'), (3, 'node_4'), (4, 'node_3'), (8, 'node_1')]

    assert "node_4" in [node[1] for node in new_ring]
    assert len([node[1] for node in new_ring]) == 4

    node_2_values = test_stores["node_2"]
    assert "c" in node_2_values

    node_1_values = test_stores["node_1"]
    assert "a" in node_1_values
    assert "b" in node_1_values

    node_3_values = test_stores["node_3"]
    assert "8" in node_3_values

    node_4_values = test_stores["node_4"]
    assert "1" in node_4_values
