import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_misnumbered_list(self):
        md = """
1. First item
2. Second item
4. Third item?
"""
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

    def test_quote_block(self):
        md = """>This is a quoted line.
>This is also a quoted line.
>Why is this quote
>so long
>for no reason."""
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.QUOTE,
        )

    def test_quote_block_some_space(self):
        md = """>This is a quoted line.
> This is also a quoted line.
>Why is this quote
> so long
> for no reason."""
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.QUOTE,
        )

    def test_unordered(self):
        md = """- banana
- apples
- bread
- peanut butter"""
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST,
        )

    def test_heading(self):
        md = """## heading 2"""
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING,
        )