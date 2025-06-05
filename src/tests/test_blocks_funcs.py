import unittest

from blocks_funcs import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdowntoBlocks(unittest.TestCase):
    # def test_three_blocks(self):
    #     doc = '''# This is a heading. 
        
    #     This is a paragraph of text.

    #     * This is the first list item in a list block. 
    #     * This is the second list item.'''
    #     actual = markdown_to_blocks(doc)
    #     expected = [
    #         "# This is a heading",
    #         "This is a paragraph of text.",
    #         "* This is the first list item in a list block. \n * This is the second list item."
    #     ]
    #     self.assertEqual(expected, actual)

    def test_white_space(self):
        doc = "   This is a block of text   "
        actual = markdown_to_blocks(doc)
        expected = ["This is a block of text"]
        self.assertEqual(expected, actual)

    def test_double_linebreak(self):
        doc = '''Or so they say
        
        What is going on?    '''
        actual = markdown_to_blocks(doc)
        expected = [
            "Or so they say",
            "What is going on?"
        ]
        self.assertEqual(expected, actual)

    def test_whitespace_blank(self):
        doc = '''This is a block of TEXT A   

        This is the next line after a blank line      '''
        actual = markdown_to_blocks(doc)
        expected = [
            "This is a block of TEXT A",
            "This is the next line after a blank line"
        ]
        self.assertEqual(expected, actual)

    def test_multiblanks(self):
        doc = '''This is a block of text B


        This is the next line after a blank line      '''
        actual = markdown_to_blocks(doc)
        expected = [
            "This is a block of text B",
            "This is the next line after a blank line"
        ]
        self.assertEqual(expected, actual)
    
    def test_headers(self):
        doc = '''
# This is an h1 header

This is some paragraph test

## This is an h2 header
'''
        actual = markdown_to_blocks(doc)
        expected = [
            "# This is an h1 header",
            "This is some paragraph test",
            "## This is an h2 header"
        ]
        self.assertEqual(expected, actual)

    def test_codeblock(self):
        doc = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        actual = markdown_to_blocks(doc)
        expected = [
            "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        ]
        self.assertEqual(expected, actual)

    def test_quoteblock(self):
        doc = """
        > Somewhere something incredible is waiting to be known
        
        Don't you agree?
        """
        actual = markdown_to_blocks(doc)
        expected = [
            "> Somewhere something incredible is waiting to be known",
            "Don't you agree?"
        ]
        self.assertEqual(expected, actual)

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

class TestBlockstoBlockType(unittest.TestCase):
    def test_heading(self):
        block = '## This is a header'
        actual = block_to_block_type(block)
        expected = BlockType.HEADING
        self.assertEqual(expected, actual)

    def test_code(self):
        block = '```This is a code block```'
        actual = block_to_block_type(block)
        expected = BlockType.CODE
        self.assertEqual(expected, actual)

    def test_quote(self):
        block = '''> This is a quote block
> It is very short
> Very insightful'''
        actual = block_to_block_type(block)
        expected = BlockType.QUOTE
        self.assertEqual(expected, actual)

    def test_unordered_list(self):
        block = '''- This is an unordered list
- It is very short
- Very insightful'''
        actual = block_to_block_type(block)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(expected, actual)

    def test_ordered_list(self):
        block = '''1. This is a numbered list
2. It is very short
3. Very insightful'''
        actual = block_to_block_type(block)
        expected = BlockType.ORDERED_LIST
        self.assertEqual(expected, actual)

    def test_paragraph(self):
        block = '''This is just a normal paragraph'''
        actual = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(expected, actual)