from app_consistent_hashing import find_node


def test_find_node():
    test_key = "test_key"
    hash_ring_size = 9
    test_ring = [(0, "node1"), (3, "node2"), (6, "node3")]
    # Hash gives 5 for this key, so it should map to node3
    assert find_node(test_key, hash_ring_size, test_ring) == "node3"


def test_find_node_wrap_around():
    test_key = "test_key_1"
    hash_ring_size = 9
    test_ring = [(0, "node1"), (3, "node2"), (6, "node3")]
    print(f"Hash for {test_key}: {hash(test_key) % hash_ring_size}")
    # Hash gives 8 for this key, so it should map to node1
    assert find_node(test_key, hash_ring_size, test_ring) == "node1"
