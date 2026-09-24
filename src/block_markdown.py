from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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