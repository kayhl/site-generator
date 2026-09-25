import unittest
from block_markdown import *

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

    def test_heading_inline(self):
        node = block_heading_to_htmlnode("## A **bold** heading")
        self.assertEqual(node.to_html(), "<h2>A <b>bold</b> heading</h2>")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
>Here's our block quote,
> it's a quote in a block.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Here's our block quote, it's a quote in a block.</blockquote></div>",
        )

    def test_unorderedblock(self):
        md = """- one
- two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two</li></ul></div>",
        )

    def test_orderedblock(self):
        md = """1. one
2. two
3. three
4. four
5. five
6. six
7. seven
8. eight
9. nine
10. ten
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one</li><li>two</li><li>three</li><li>four</li><li>five</li><li>six</li><li>seven</li><li>eight</li><li>nine</li><li>ten</li></ol></div>",
        )