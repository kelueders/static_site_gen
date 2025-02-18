import unittest

from blocks_funcs import markdown_to_blocks

class TestMarkdowntoBlocks(unittest.TestCase):
    def test_three_blocks(self):
        doc = "# This is a heading\n\nThis is a paragraph of text.\n\n* This is the first list item in a list block. \n * This is the second list item."
        actual = markdown_to_blocks(doc)
        expected = [
            "# This is a heading",
            "This is a paragraph of text.",
            "* This is the first list item in a list block. \n * This is the second list item."
        ]
        self.assertEqual(expected, actual)