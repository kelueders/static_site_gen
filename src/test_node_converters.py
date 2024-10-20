import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType
from node_converters import text_node_to_html_node

class TestNodeConverters(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        node = TextNode("This is text", TextType.TEXT)
        expected = LeafNode(tag=None, value='This is text', props=None)
        self.assertEqual(expected, text_node_to_html_node(node))

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This text is bold", TextType.BOLD)
        expected = LeafNode(tag='b', value='This text is bold', props=None)
        self.assertEqual(expected, text_node_to_html_node(node))

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This text is italic", TextType.ITALIC)
        expected = LeafNode(tag='i', value='This text is italic', props=None)
        self.assertEqual(expected, text_node_to_html_node(node))

    def test_text_node_to_html_node_link(self):
        node = TextNode("Google", TextType.LINK, "Google.com")
        expected = LeafNode(tag='a', value="Google", props={"href": "Google.com"})
        self.assertEqual(expected, text_node_to_html_node(node))

    def test_text_node_to_html_node_image(self):
        node = TextNode("Google Logo", TextType.IMAGE, "Google.com")
        expected = LeafNode(tag='img', value="", props={"src": "Google.com", "alt": "Google Logo"})
        self.assertEqual(expected, text_node_to_html_node(node))

    def test_text_node_to_html_raises_error(self):
        with self.assertRaises(TypeError):
            node = TextNode("p", "blah")
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()