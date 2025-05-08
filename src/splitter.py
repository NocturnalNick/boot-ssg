from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits all TextType.NORMAL nodes in old_nodes by the given delimiter, returning a new list of nodes where text between delimiters is assigned text_type, and other text is kept as NORMAL.
    If a delimiter is unmatched, raises ValueError.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Outside delimiter: keep as NORMAL
                new_nodes.append(TextNode(part, TextType.NORMAL))
            else:
                # Inside delimiter: assign given text_type
                new_nodes.append(TextNode(part, text_type))
    return new_nodes
