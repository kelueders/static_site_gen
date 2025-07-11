import unittest

from markdown_to_html import markdown_to_html_node, determine_heading_tag, text_to_children, strip_block_of_mdsyntax, get_list_children
from nodes.leafnode import LeafNode
from blocks_funcs import BlockType

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

    ''''
    ***************TESTS FOR text_to_children()*************
    '''
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

    def test_no_children(self):
        text = "This is just a paragraph"
        actual = text_to_children(text)
        expected = 0
        self.assertEqual(expected, actual)

    '''
    *********TESTS for get_list_children()********
    '''
    def test_get_list_children_unordered(self):
        block = '''- This is an unordered list\n- It is very short\n- Very insightful'''
        actual = get_list_children(block, BlockType.UNORDERED_LIST)
        expected = [
            LeafNode(tag='li', value='This is an unordered list'),
            LeafNode(tag='li', value='It is very short'),
            LeafNode(tag='li', value='Very insightful')
        ]
        self.assertEqual(expected, actual)

    def test_get_list_children_ordered(self):
        block = '''1. This is an ordered list\n2. It is very short\n3. Very clever'''
        actual = get_list_children(block, BlockType.ORDERED_LIST)
        expected = [
            LeafNode(tag='li', value='This is an ordered list'),
            LeafNode(tag='li', value='It is very short'),
            LeafNode(tag='li', value='Very clever')
        ]
        self.assertEqual(expected, actual)

    def test_get_list_children_fruit(self):
        block = '''- Peaches\n- Bananas\n- Apples'''
        actual = get_list_children(block, BlockType.UNORDERED_LIST)
        expected = [
            LeafNode(tag='li', value='Peaches'),
            LeafNode(tag='li', value='Bananas'),
            LeafNode(tag='li', value='Apples')
        ]
        self.assertEqual(expected, actual)

''''
***************TESTS FOR strip_block_of_mdsyntax()*************
'''
class TestStripBlock(unittest.TestCase):
    def test_code(self):
        block = "```This is a code block```"
        expected = "This is a code block"
        self.assertEqual(strip_block_of_mdsyntax(block, BlockType.CODE), expected)

    def test_code_multilines(self):
        block = """
```
This is a code block
```
"""
        expected = "This is a code block"
        self.assertEqual(strip_block_of_mdsyntax(block, BlockType.CODE), expected)

    def test_code_multilines_inside(self):
        block = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        expected = "This is text that _should_ remain\nthe **same** even with inline stuff"
        self.assertEqual(strip_block_of_mdsyntax(block, BlockType.CODE), expected)

    def test_headers(self):
        block = "# This is an h1 header"
        expected = "This is an h1 header"
        self.assertEqual(strip_block_of_mdsyntax(block, BlockType.HEADING), expected)

    def test_paragraphs(self):
        block = "This is a **bolded**\nparagraph text \nin a p tag here"
        expected = "This is a **bolded**\nparagraph text \nin a p tag here"
        self.assertEqual(strip_block_of_mdsyntax(block, BlockType.PARAGRAPH), expected)

''''
***************TESTS FOR markdown_to_html_node()*************
'''
class TestMarkdowntoHtmlnode(unittest.TestCase):

    def test_paragraphs_basic(self):
        md = """
This is **bolded** paragraph text in a p tag here

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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
## Grocery List

- Peaches
- Bananas
- Apples
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Grocery List</h2><ul><li>Peaches</li><li>Bananas</li><li>Apples</li></ul></div>",
        )

if __name__ == "__main__":
    unittest.main()