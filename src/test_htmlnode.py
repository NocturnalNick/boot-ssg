import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "text"})
        expected = "HTMLNode(tag='p', value='Hello', children=[], props={'class': 'text'})"
        self.assertEqual(repr(node), expected)

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("p", "Hello", None, {"class": "text", "id": "greeting"})
        expected = ' class="text" id="greeting"'
        self.assertEqual(node.props_to_html(), expected)

    def test_leaf_node_to_html(self):
        leaf = LeafNode("p", "Hello", {"class": "text"})
        expected = '<p class="text">Hello</p>'
        self.assertEqual(leaf.to_html(), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_node_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()
            
    def test_leaf_node_no_tag(self):
        leaf = LeafNode(None, "Just some text")
        self.assertEqual(leaf.to_html(), "Just some text")
        
    def test_leaf_node_link(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.example.com"})
        self.assertEqual(leaf.to_html(), '<a href="https://www.example.com">Click me!</a>')

if __name__ == "__main__":
    unittest.main()