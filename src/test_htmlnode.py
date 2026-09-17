import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "Click me", None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        result = node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(result, expected) 

    def test_empty_props_dict(self):
        node = HTMLNode("a", "Click me", None, {})
        result = node.props_to_html()
        expected = ""
        self.assertEqual(result, expected)

    def test_props_none(self):
        node = HTMLNode("a", "Click me", None, None)
        result = node.props_to_html()
        expected = ""
        self.assertEqual(result, expected)