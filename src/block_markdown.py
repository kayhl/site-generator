from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# NOTE: "language-tagged fences"
# Ex. ```python\nfoo\n``` treated as paragraph by block_to_block_type
# Adding support requires changing both block_to_block_type and block_code_to_htmlnode

def block_to_block_type(markdown):
    if markdown.startswith("#"):
        count = 0
        for i in markdown:
            if i != "#":
                break
            count += 1
        if 1 <= count <= 6 and len(markdown) > count:
            next = markdown[count]
            if next == " ":
                return BlockType.HEADING
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    if markdown.startswith(">"):
        lines = markdown.split("\n")
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
    if markdown.startswith("- "):
        lines = markdown.split("\n")
        if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
    if markdown.startswith("1. "):
        lines = markdown.split("\n")
        count = 1
        ordered = True
        for line in lines:
            prefix = f"{count}. "
            if not line.startswith(prefix):
                ordered = False
                break
            count += 1
        if ordered:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        clean_blocks.append(block)
    return clean_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            block_nodes.append(block_heading_to_htmlnode(block))
        elif block_type == BlockType.PARAGRAPH:
            block_nodes.append(block_paragraph_to_htmlnode(block))
        elif block_type == BlockType.CODE:
            block_nodes.append(block_code_to_htmlnode(block))
        elif block_type == BlockType.QUOTE:
            block_nodes.append(block_quote_to_htmlnode(block))
        elif block_type == BlockType.UNORDERED_LIST:
            block_nodes.append(block_unordered_to_htmlnode(block))
        elif block_type == BlockType.ORDERED_LIST:
            block_nodes.append(block_ordered_to_htmlnode(block))
        else:
            raise Exception("No matching BlockType")
    return ParentNode("div", block_nodes)

def text_to_children(text):
    children = text_to_textnodes(text)
    children_html = []
    for child in children:
        child_html = text_node_to_html_node(child)
        children_html.append(child_html)
    return children_html

def block_heading_to_htmlnode(markdown):
    heading_split = markdown.split(" ", 1)
    marker = heading_split[0]
    heading_size = len(marker)
    if marker != "#" * heading_size or not (1 <= heading_size <= 6):
        raise Exception("Incorrect Heading markdown")
    if len(heading_split) < 2:
        raise ValueError("Empty Heading")
    children_html = text_to_children(heading_split[1])
    heading_node = ParentNode(f"h{heading_size}", children_html)
    return heading_node

def block_paragraph_to_htmlnode(markdown):
    text = markdown.replace("\n", " ")
    children_html = text_to_children(text)
    paragraph_node = ParentNode("p", children_html)
    return paragraph_node

def block_code_to_htmlnode(markdown):
    text = markdown.removeprefix("```\n")
    text = text.removesuffix("```")
    text_node = TextNode(text, TextType.CODE)
    main_node = text_node_to_html_node(text_node)
    code_node = ParentNode("pre", [main_node])
    return code_node

def block_quote_to_htmlnode(markdown):
    lines = markdown.split("\n")
    clean_lines = []
    for line in lines:
        clean_lines.append(line.lstrip(">").strip())
    text = " ".join(clean_lines)
    children = text_to_children(text)
    block_node = ParentNode("blockquote", children)
    return block_node

def block_unordered_to_htmlnode(markdown):
    clean_lines = []
    for line in markdown.split("\n"):
        clean_lines.append(line.removeprefix("- "))
    li_node_list = []
    for line in clean_lines:
        children = text_to_children(line)
        li_node = ParentNode("li", children)
        li_node_list.append(li_node)
    unordered_node = ParentNode("ul", li_node_list)
    return unordered_node

def block_ordered_to_htmlnode(markdown):
    lines = markdown.split("\n")
    li_node_list = []
    for number, line in enumerate(lines, start = 1):
        line = line.removeprefix(f"{number}. ")
        children = text_to_children(line)
        li_node = ParentNode("li", children)
        li_node_list.append(li_node)
    ordered_node = ParentNode("ol", li_node_list)
    return ordered_node