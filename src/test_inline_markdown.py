import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

class TestImagesLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_image_and_link_split(self):
        node = TextNode(
            "This has both a [link](https://www.youtube.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This has both a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.youtube.com"),
                TextNode(" and an ", TextType.PLAIN), 
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_not_image(self):
        node = TextNode("This has a [link](https://boot.dev) instead of an image", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This has a [link](https://boot.dev) instead of an image", TextType.PLAIN),
            ],
            new_nodes,
        )