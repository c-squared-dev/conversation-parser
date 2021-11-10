import uuid


def generate_uuid():
    return str(uuid.uuid4())


def find_node(nodes_map, from_row_id, condition):
    for _, node in nodes_map.items():
        from_row_ids = node._from.split(';')

        if (from_row_id in from_row_ids) and node.condition == condition:
            return node
