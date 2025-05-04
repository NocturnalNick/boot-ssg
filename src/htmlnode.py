from typing import override
from textnode import TextNode, TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f"children={self.children!r}, props={self.props!r})"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return f'{self.value}'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError("Expected a TextNode instance")

    t = text_node.text_type
    if t == TextType.NORMAL:
        return LeafNode(None, text_node.text)
    elif t == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif t == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif t == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif t == TextType.LINK:
        if not text_node.url:
            raise ValueError("Link TextNode requires a url")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif t == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("Image TextNode requires a url")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception(f"Unknown TextType: {t}")

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        if not tag:
            raise ValueError("Tag cannot be None or empty")
        if children is None:
            raise ValueError("Children cannot be None")
        super().__init__(tag, value=None, props=props)
        self.children = children

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Tag cannot be None or empty")

        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html