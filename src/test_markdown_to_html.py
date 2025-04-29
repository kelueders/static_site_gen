import unittest

from markdown_to_html import markdown_to_html_node, determine_heading_tag, get_list_children, block_to_htmlnode, text_to_children
from htmlnode import HTMLNode
from leafnode import LeafNode
from blocks_funcs import BlockType, block_to_block_type

class TestHelpers(unittest.TestCase):
    '''
    ********TESTS for determine_heading_tag()********
    '''
    def test_determine_heading_tag_h2(self):
        block = "## This is a h2 header"
        actual = determine_heading_tag(block)
        expected = "h2"
        self.assertEqual(expected, actual)

    def test_determine_heading_tag_h6(self):
        block = "###### This is a h6 header"
        actual = determine_heading_tag(block)
        expected = "h6"
        self.assertEqual(expected, actual)

    '''
    *********TESTS for get_list_children()********
    '''
    def test_get_list_children_unordered(self):
        block = '''- This is an unordered list
- It is very short
- Very insightful'''
        actual = get_list_children(block)
        expected = [
            HTMLNode(tag='li', value='- This is an unordered list'),
            HTMLNode(tag='li', value='- It is very short'),
            HTMLNode(tag='li', value='- Very insightful')
        ]
        self.assertEqual(expected, actual)

    def test_get_list_children_ordered(self):
        block = '''1. This is an ordered list
2. It is very short
3. Very clever'''
        actual = get_list_children(block)
        expected = [
            HTMLNode(tag='li', value='1. This is an ordered list'),
            HTMLNode(tag='li', value='2. It is very short'),
            HTMLNode(tag='li', value='3. Very clever')
        ]
        self.assertEqual(expected, actual)

    '''
    ********TESTS for block_to_htmlnode()********
    '''
    def test_block_to_html_node_p(self):
        block = "This is **bolded** paragraph text in a p tag here"
        block_type = block_to_block_type(block)
        actual = block_to_htmlnode(block, block_type)
        expected = HTMLNode('p', 'This is **bolded** paragraph text in a p tag here')
        self.assertEqual(expected, actual)

    def test_block_to_html_node_heading(self):
        block = "## This is a header 2"
        block_type = block_to_block_type(block)
        actual = block_to_htmlnode(block, block_type)
        expected = HTMLNode('h2', 'This is a header 2')
        self.assertEqual(expected, actual)

    def test_block_to_html_node_code(self):
        block = """```This is text that _should_ remain the **same** even with inline stuff```"""
        block_type = block_to_block_type(block)
        actual = block_to_htmlnode(block, block_type)
        expected = HTMLNode('pre', '<code>This is text that _should_ remain the **same** even with inline stuff</code>')
        self.assertEqual(expected, actual)

    def test_block_to_html_node_unordered(self):
        block = '''- This is an unordered list
- It is very short
- Very insightful'''
        block_type = block_to_block_type(block)
        actual = block_to_htmlnode(block, block_type)
        children = [
            HTMLNode(tag='li', value='- This is an unordered list'),
            HTMLNode(tag='li', value='- It is very short'),
            HTMLNode(tag='li', value='- Very insightful')
        ]
        expected = HTMLNode('ul', '- This is an unordered list\n- It is very short\n- Very insightful', children)
        self.assertEqual(expected, actual)

    def test_block_to_html_node_ordered(self):
        block = '''1. This is an ordered list
2. It is very short
3. Very clever'''
        block_type = block_to_block_type(block)
        actual = block_to_htmlnode(block, block_type)
        children = [
            HTMLNode(tag='li', value='1. This is an ordered list'),
            HTMLNode(tag='li', value='2. It is very short'),
            HTMLNode(tag='li', value='3. Very clever')
        ]
        expected = HTMLNode('ol', '1. This is an ordered list\n2. It is very short\n3. Very clever', children)
        self.assertEqual(expected, actual)

    def test_text_to_children(self):
        text = "This is another paragraph with _italic_ text and `code` here"
        actual = text_to_children(text)
        expected = [
            LeafNode(None, "This is another paragraph with "),
            LeafNode("i", "italic"),
            LeafNode(None, " text and "),
            LeafNode("code", "code" ),
            LeafNode(None, " here")
        ]
        self.assertEqual(expected, actual)

class TestMarkdowntoHtmlnode(unittest.TestCase):
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