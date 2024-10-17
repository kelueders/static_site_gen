import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag = "a", value = "Google", props = {"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expected, node.props_to_html())

    def test_props_to_html_novalue(self):
        node = HTMLNode(tag = "body", props = {"style": "background-color:powderblue"})
        expected = ' style="background-color:powderblue"'
        self.assertEqual(expected, node.props_to_html())

    def test_props_to_html_noprops(self):
        node = HTMLNode(tag = "table")
        expected = ""
        self.assertEqual(expected, node.props_to_html())

    def test_to_html_raises_error(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode(tag = "a", value = "Google", props = {"href": "https://www.google.com", "target": "_blank"})
            node.to_html()

if __name__ == "__main__":
    unittest.main()