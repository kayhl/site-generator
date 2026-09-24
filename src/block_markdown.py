def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        clean_blocks.append(block)
    return clean_blocks