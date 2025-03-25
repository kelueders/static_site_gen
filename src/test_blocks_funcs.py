import unittest

from blocks_funcs import markdown_to_blocks

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