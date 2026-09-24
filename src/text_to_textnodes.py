from inline_markdown import *
from textnode import TextNode, TextType


def text_to_textnodes(text):
    node = TextNode(text, TextType.PLAIN)
    split_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_images = split_nodes_image(split_code)
    split_links = split_nodes_link(split_images)
    return split_links
