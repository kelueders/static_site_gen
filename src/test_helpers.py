import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType
from helpers import text_node_to_html_node, split_nodes_delimiter
from split_images_links import extract_markdown_images, extract_markdown_links

'''
Test the text_node_to_html function.
'''
class TestTextNodetoHtmlNode(unittest.TestCase):
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
        with self.assertRaises(AttributeError):
            node = TextNode("p", 12)
            text_node_to_html_node(node)

'''
Test the split_nodes_delimiter() function.
'''
class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
            ]
        self.assertEqual(expected, actual)

    def test_split_delimiter_italics(self):
        node = TextNode("I love putting things in *italics*!", TextType.TEXT)
        actual = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("I love putting things in ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
            TextNode("!", TextType.TEXT)
        ]
        self.assertEqual(expected, actual)

    def test_split_delimiter_bold(self):
        node = TextNode("Yay for **bold** font!", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Yay for ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" font!", TextType.TEXT)
        ]
        self.assertEqual(expected, actual)

    def test_split_delimiter_multiple_nodes(self):
        node1 = TextNode("Wahoo there is **bold** font AND", TextType.TEXT)
        node2 = TextNode("There is a `code block` section!", TextType.TEXT)
        after_bold = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        after_code = split_nodes_delimiter(after_bold, "`", TextType.CODE)
        expected = [
            TextNode("Wahoo there is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" font AND", TextType.TEXT),
            TextNode("There is a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" section!", TextType.TEXT),
        ]
        self.assertEqual(expected, after_code)

    def test_text_node_to_html_raises_error(self):
        with self.assertRaises(Exception):
            node = TextNode("Yay!", TextType.BOLD)
            split_nodes_delimiter(node)

class TestExtractImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(expected, actual)

class TestExtractLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()