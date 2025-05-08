import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        # Single image
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png")
        ], matches)

        # Multiple images
        matches = extract_markdown_images(
            "![alt1](url1) and ![alt2](url2)"
        )
        self.assertListEqual([
            ("alt1", "url1"),
            ("alt2", "url2")
        ], matches)

        # No images
        matches = extract_markdown_images("No images here!")
        self.assertListEqual([], matches)

        # Empty alt text
        matches = extract_markdown_images("![](url3)")
        self.assertListEqual([
            ("", "url3")
        ], matches)

        # Image with spaces in alt and url
        matches = extract_markdown_images("![alt text here](http://example.com/img.png)")
        self.assertListEqual([
            ("alt text here", "http://example.com/img.png")
        ], matches)

    def test_extract_markdown_links(self):
        # Single link
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([
            ("link", "https://www.example.com")
        ], matches)

        # Multiple links
        matches = extract_markdown_links(
            "[one](url1) and [two](url2)"
        )
        self.assertListEqual([
            ("one", "url1"),
            ("two", "url2")
        ], matches)

        # No links
        matches = extract_markdown_links("No links here!")
        self.assertListEqual([], matches)

        # Link with spaces in anchor and url
        matches = extract_markdown_links("[anchor text](http://example.com/page)")
        self.assertListEqual([
            ("anchor text", "http://example.com/page")
        ], matches)

        # Should not match images
        matches = extract_markdown_links("![alt](url)")
        self.assertListEqual([], matches)

        # Mixed links and images
        matches = extract_markdown_links("[real link](url) and ![alt](imgurl)")
        self.assertListEqual([
            ("real link", "url")
        ], matches)

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
