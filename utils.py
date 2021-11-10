import uuid


def generate_uuid():
    return str(uuid.uuid4())


def find_node(nodes_map, from_row_id, condition):
    for _, node in nodes_map.items():
        if node._from == from_row_id and node.condition == condition:
            return node
