import unittest

from nodes.leafnode import LeafNode
from nodes.textnode import TextNode, TextType
from helpers import text_node_to_html_node, split_nodes_delimiter, text_to_textnodes

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
    
    def test_text_node_to_html_node_code(self):
        node = TextNode("This text is code", TextType.CODE)
        expected = LeafNode(tag='code', value='This text is code', props=None)
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

    def test_split_delimiter_multiword_bold(self):
        node = TextNode("Yay for **bolded words** font!", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Yay for ", TextType.TEXT),
            TextNode("bolded words", TextType.BOLD),
            TextNode(" font!", TextType.TEXT)
        ]
        self.assertEqual(expected, actual)

    def test_split_delimiter_multiword_two_bold(self):
        node = TextNode("Yay for **bolded words** and **more bolded** words!", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Yay for ", TextType.TEXT),
            TextNode("bolded words", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bolded", TextType.BOLD),
            TextNode(" words!", TextType.TEXT)
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

    def test_split_delimiter_blank(self):
        node = TextNode("", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = []
        self.assertEqual(expected, actual)

    def test_split_delimiter_invalid(self):
        with self.assertRaises(ValueError) as cm:
            node = TextNode("This **INVALID!", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.TEXT)
        invalid_markdown = cm.exception
        self.assertEqual(str(invalid_markdown), "That's invalid Markdown syntax. Formatted section not closed.")

'''
Test text_to_textnodes() function
'''
class TestTexttoTextNode(unittest.TestCase):
    def test_text_to_textnodes_all(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(expected, actual)

    def test_text_to_textnodes_italiccode(self):
        text = "This is another paragraph with *italic* text and `code` here"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is another paragraph with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT)
        ]


if __name__ == "__main__":
    unittest.main()