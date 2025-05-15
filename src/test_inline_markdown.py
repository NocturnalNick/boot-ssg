import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    markdown_to_blocks,
    markdown_to_html_node,
    extract_title,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        node = TextNode("No images here!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("No images here!", TextType.TEXT)], new_nodes)

    def test_split_images_single(self):
        node = TextNode("Only one ![img](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("Only one ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url")
        ], new_nodes)

    def test_split_images_edge(self):
        node = TextNode("![img1](url1) and ![img2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2")
        ], new_nodes)

    def test_split_images_consecutive(self):
        node = TextNode("![a](u1)![b](u2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("a", TextType.IMAGE, "u1"),
            TextNode("b", TextType.IMAGE, "u2")
        ], new_nodes)

    def test_split_images_nontext(self):
        node = TextNode("not an image", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("No links here!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("No links here!", TextType.TEXT)], new_nodes)

    def test_split_links_single(self):
        node = TextNode("Only [one](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("Only ", TextType.TEXT),
            TextNode("one", TextType.LINK, "url")
        ], new_nodes)

    def test_split_links_edge(self):
        node = TextNode("[one](url1) and [two](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("one", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.LINK, "url2")
        ], new_nodes)

    def test_split_links_consecutive(self):
        node = TextNode("[a](u1)[b](u2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("a", TextType.LINK, "u1"),
            TextNode("b", TextType.LINK, "u2")
        ], new_nodes)

    def test_split_links_nontext(self):
        node = TextNode("not a link", TextType.IMAGE, "url")
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

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

    def test_text_to_textnodes(self):
        from inline_markdown import text_to_textnodes
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected)

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

    def test_extract_title(self):
        md = "# Hello World\nSome content"
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_missing(self):
        md = "No header here\n#Not h1"
        with self.assertRaises(ValueError):
            extract_title(md)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_blocks(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### H6 heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Multiple # heading"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("####### Too many hashes"), BlockType.HEADING)

    def test_code_blocks(self):
        self.assertEqual(block_to_block_type("""```
code here
```"""), BlockType.CODE)
        self.assertEqual(block_to_block_type("""```
print('hi')
print('bye')
```"""), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("``\nnot a code block\n``"), BlockType.CODE)

    def test_quote_blocks(self):
        self.assertEqual(block_to_block_type("> quoted line"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> line1\n> line2"), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type("> not quoted\nnot quoted"), BlockType.QUOTE)

    def test_unordered_list_blocks(self):
        self.assertEqual(block_to_block_type("- item1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- item1\n- item2"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("- item1\nitem2"), BlockType.UNORDERED_LIST)

    def test_ordered_list_blocks(self):
        self.assertEqual(block_to_block_type("1. first"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1. first\n3. third"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("0. zero\n1. one"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1. one\n2. two\n2. not incremented"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1. one\ntwo. not a number"), BlockType.ORDERED_LIST)

    def test_paragraph_blocks(self):
        self.assertEqual(block_to_block_type("Just some text."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("This is a paragraph\nwith multiple lines."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("No special markdown here."), BlockType.PARAGRAPH)

    def test_ambiguous_blocks(self):
        # Looks like heading but too many hashes
        self.assertEqual(block_to_block_type("####### Not heading"), BlockType.PARAGRAPH)
        # Looks like code but not triple backtick
        self.assertEqual(block_to_block_type("``\nnot code\n``"), BlockType.PARAGRAPH)
        # Looks like unordered but one line is not
        self.assertEqual(block_to_block_type("- item1\nnot a list"), BlockType.PARAGRAPH)
        # Looks like ordered but numbering is wrong
        self.assertEqual(block_to_block_type("1. one\n3. three"), BlockType.PARAGRAPH)

from inline_markdown import block_to_block_type, BlockType

if __name__ == "__main__":
    unittest.main()
