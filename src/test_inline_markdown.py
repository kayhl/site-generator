import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_no_delimiter(self):
        with self.assertRaises(Exception):
            split = split_nodes_delimiter([TextNode("Text with no delimiter", TextType.PLAIN)], None, TextType.PLAIN)

    def test_missing_delimiter(self):
        split = split_nodes_delimiter([TextNode("Text with no delimiter", TextType.PLAIN)], "**", TextType.PLAIN)
        self.assertEqual(split[0], TextNode("Text with no delimiter", TextType.PLAIN))

    def test_bold_delimiter(self):
        split = split_nodes_delimiter([TextNode("Text with **bold** delimiter", TextType.PLAIN)], "**", TextType.BOLD)
        self.assertEqual(split[0], TextNode("Text with ", TextType.PLAIN))
        self.assertEqual(split[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(split[2], TextNode(" delimiter", TextType.PLAIN))

    def test_integers_without_text(self):
        with self.assertRaises(AttributeError):
            split = split_nodes_delimiter([TextNode(123, TextType.PLAIN)], "`", TextType.PLAIN)