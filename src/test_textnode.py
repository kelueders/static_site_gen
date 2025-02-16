import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_type(self):
        node = TextNode("Testing text", TextType.BOLD, "http://google.com")
        node2 = TextNode("Testing text", TextType.ITALIC, "http://google.com")
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("Testing text", TextType.BOLD, "http://google.com")
        node2 = TextNode("Testing text", TextType.BOLD, None)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Testing text", TextType.BOLD, "http://google.com")
        node2 = TextNode("Testing text", TextType.BOLD, "http://google.com")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("Testing text yay!", TextType.BOLD, "http://google.com")
        node2 = TextNode("Testing text", TextType.BOLD, "http://google.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Testing text", TextType.BOLD, "http://google.com")
        self.assertEqual("TextNode(Testing text, TextType.BOLD, http://google.com)", repr(node))

if __name__ == "__main__":
    unittest.main()