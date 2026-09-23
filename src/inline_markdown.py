from textnode import TextType, TextNode, text_node_to_html_node

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        if node.text_type == TextType.PLAIN:
            node_split = node.text.split(delimiter)
            if len(node_split) % 2 != 0:
                for index, value in enumerate(node_split):
                    if index % 2 == 0:
                        if value:
                            new_nodes.append(TextNode(value, TextType.PLAIN))
                    else:
                        if value:
                            new_nodes.append(TextNode(value, text_type))
            else:
                raise Exception("Missing delimiter - invalid Markdown syntax")
    return new_nodes