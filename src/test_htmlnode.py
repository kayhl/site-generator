import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p","This is a paragraph")
        result = node.to_html()
        expected = "<p>This is a paragraph</p>"
        self.assertEqual(result, expected)

    def test_leaf_to_hyperlink(self):
        node = LeafNode("a", "Click here", {"href": "https://www.google.com"})
        result = node.to_html()
        expected = '<a href="https://www.google.com">Click here</a>'
        self.assertEqual(result, expected)

    def test_value_none(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p","")
            node.to_html()

    def test_tag_none(self):
        node = LeafNode("","some value")
        result = node.to_html()
        expected = "some value"
        self.assertEqual(result, expected)

    def test_leaf_repr(self):
        node = LeafNode("a","Click here", {"href": "https://www.google.com"})
        result = node.__repr__()
        expected = 'tag: a, value: Click here, props as html:  href="https://www.google.com"'
        self.assertEqual(result, expected)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiples(self):
        child_one = LeafNode("i", "child one")
        child_two = LeafNode("b", "child two")
        children = [child_one, child_two]
        parent_node = ParentNode("p", children)
        self.assertEqual(parent_node.to_html(), "<p><i>child one</i><b>child two</b></p>")

    def test_to_html_props(self):
        child_node = LeafNode("b", "Click here")
        children = [child_node]
        parent_node = ParentNode("a", children, {"href": "https://www.google.com"})
        result = parent_node.to_html()
        expected = '<a href="https://www.google.com"><b>Click here</b></a>'
        self.assertEqual(result, expected)

    def test_no_children_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_no_tag_error(self):
        child_node = LeafNode("p", "child")
        children = [child_node]
        with self.assertRaises(ValueError):
            ParentNode("", children).to_html()

    def test_parent_repr(self):
        child_one = LeafNode("u", "underlined child")
        child_two = LeafNode("i", "italicized child")
        children = [child_one, child_two]
        parent_node = ParentNode("a", children, {"href": "https://www.google.com"})
        result = parent_node.__repr__()
        expected = 'tag: a, children: [tag: u, value: underlined child, props as html: , tag: i, value: italicized child, props as html: ], props as html:  href="https://www.google.com"'
        self.assertEqual(result, expected)