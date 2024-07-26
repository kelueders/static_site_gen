import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_noprops(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = '<p>This is a paragraph of text.</p>'
        self.assertEqual(expected, node.to_html())

    def test_to_html_withprops(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(expected, node.to_html())

    def test_to_html_notag(self):
        node = LeafNode(tag = None, value = "This is a paragraph of text.")
        expected = "This is a paragraph of text."
        self.assertEqual(expected, node.to_html())

    def test_to_html_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

if __name__ == "__main__":
    unittest.main()