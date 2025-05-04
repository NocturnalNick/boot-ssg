import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "text"})
        expected = "HTMLNode(tag='p', value='Hello', children=[], props={'class': 'text'})"
        self.assertEqual(repr(node), expected)

    def test_text_node_to_html_node_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_text_node_to_html_node_code(self):
        node = TextNode("code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code snippet")

    def test_text_node_to_html_node_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://img.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://img.com/img.png", "alt": "Alt text"})

    def test_text_node_to_html_node_invalid(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node("not a textnode")

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

    def test_parent_node_no_tag(self):
        with self.assertRaisesRegex(ValueError, "Tag cannot be None or empty"):
            ParentNode(None, [])

    def test_parent_node_no_children(self):
        with self.assertRaisesRegex(ValueError, "Children cannot be None"):
            ParentNode("div", None)

    def test_parent_node_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_parent_node_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><b>child2</b></div>")

    def test_parent_node_nested_parents(self):
        grandchild_node = LeafNode("i", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><i>grandchild</i></span></div>")

    def test_parent_node_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props={"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span></div>')

if __name__ == "__main__":
    unittest.main()