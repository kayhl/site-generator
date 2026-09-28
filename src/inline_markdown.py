import re
from textnode import TextType, TextNode

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 title found")

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

def extract_markdown_images(text):
    image_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_matches

def extract_markdown_links(text):
    link_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:        
        current_text = node.text
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        if node.text_type == TextType.PLAIN:
            image_matches = extract_markdown_images(node.text)
            if not image_matches:
                new_nodes.append(node)
                continue
            for match in image_matches:
                node_split = current_text.split(f"![{match[0]}]({match[1]})", 1)
                if node_split[0]:
                    new_nodes.append(TextNode(f"{node_split[0]}", TextType.PLAIN))
                new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
                current_text = node_split[1]
            if current_text:
                new_nodes.append(TextNode(f"{current_text}", TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:        
        current_text = node.text
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        if node.text_type == TextType.PLAIN:
            link_matches = extract_markdown_links(node.text)
            if not link_matches:
                new_nodes.append(node)
                continue
            for match in link_matches:
                node_split = current_text.split(f"[{match[0]}]({match[1]})", 1)
                if node_split[0]:
                    new_nodes.append(TextNode(f"{node_split[0]}", TextType.PLAIN))
                new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
                current_text = node_split[1]
            if current_text:
                new_nodes.append(TextNode(f"{current_text}", TextType.PLAIN))
    return new_nodes