from textnode import TextNode, TextType
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    """
    Determines the type of markdown block.
    Assumes block is stripped of leading/trailing whitespace.
    """
    lines = block.split("\n")
    # Heading: starts with 1-6 #, then space
    if len(lines) == 1 and re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    # Code block: starts and ends with 3 backticks
    if lines[0].startswith("```") and lines[-1].startswith("```") and len(lines) >= 2:
        return BlockType.CODE
    # Quote: every line starts with '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    # Unordered list: every line starts with '- '
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    # Ordered list: every line starts with incrementing number, dot, space
    is_ordered = True
    for idx, line in enumerate(lines):
        if not re.match(rf"^{idx+1}\. ", line):
            is_ordered = False
            break
    if is_ordered and len(lines) > 0:
        return BlockType.ORDERED_LIST
    # Default: paragraph
    return BlockType.PARAGRAPH


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text):
    """
    Converts a markdown-flavored text string into a list of TextNode objects.
    Handles images, links, bold (**), italic (_), and code (`) formatting.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    # Order: image, link, bold, italic, code
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return [node for node in nodes if node.text or node.text_type in (TextType.IMAGE, TextType.LINK)]
def extract_markdown_images(text):
    """
    Extracts markdown images from text.
    Returns a list of (alt, url) tuples.
    """
    pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
    return re.findall(pattern, text)


def extract_markdown_links(text):
    """
    Extracts markdown links from text.
    Returns a list of (anchor, url) tuples.
    Skips images (does not match links that start with ![).
    """
    pattern = r'(?<!!)\[([^\]]+)\]\(([^\)]+)\)'
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    """
    Splits TextNodes of type TEXT into sequences of TextNodes based on markdown images.
    For example, 'text ![alt](url) text' -> [TEXT, IMAGE, TEXT]
    """
    new_nodes = []
    image_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        last_idx = 0
        for match in re.finditer(image_pattern, text):
            start, end = match.span()
            alt, url = match.groups()
            if start > last_idx:
                pre_text = text[last_idx:start]
                if pre_text:
                    new_nodes.append(TextNode(pre_text, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            last_idx = end
        if last_idx < len(text):
            post_text = text[last_idx:]
            if post_text:
                new_nodes.append(TextNode(post_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    """
    Splits TextNodes of type TEXT into sequences of TextNodes based on markdown links.
    For example, 'text [anchor](url) text' -> [TEXT, LINK, TEXT]
    """
    new_nodes = []
    link_pattern = r'(?<!!)\[([^\]]+)\]\(([^\)]+)\)'
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        last_idx = 0
        for match in re.finditer(link_pattern, text):
            start, end = match.span()
            anchor, url = match.groups()
            if start > last_idx:
                pre_text = text[last_idx:start]
                if pre_text:
                    new_nodes.append(TextNode(pre_text, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            last_idx = end
        if last_idx < len(text):
            post_text = text[last_idx:]
            if post_text:
                new_nodes.append(TextNode(post_text, TextType.TEXT))
    return new_nodes


def markdown_to_blocks(markdown):
    """
    Splits a raw Markdown string into a list of block strings, separated by double newlines.
    Each block is stripped of leading/trailing whitespace; empty blocks are removed.
    """
    # Normalize newlines
    blocks = markdown.split("\n\n")
    result = [block.strip() for block in blocks if block.strip() != ""]
    return result

