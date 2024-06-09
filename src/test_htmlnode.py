import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag = "a", value = "Google", props = {"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expected, node.props_to_html())

    def test_to_html(self):
        node = HTMLNode(tag = "a", value = "Google", props = {"href": "https://www.google.com", "target": "_blank"})
        self.assertRaises(NotImplementedError, node.to_html())

if __name__ == "__main__":
    unittest.main()