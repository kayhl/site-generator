import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("Empty link", TextType.LINK, "None")
        node2 = TextNode("Empty link", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Testing", TextType.BOLD)
        node2 = TextNode("Testing", TextType.ITALIC)
        self.assertNotEqual(node, node2)


class TestTextType(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def text_image(self):
        node = TextNode("alt text here", TextType.IMAGE, "https://images.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.url, "https://images.google.com")


if __name__ == "__main__":
    unittest.main()
