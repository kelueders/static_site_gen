import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_type(self):
        node = TextNode("Testing text", "bold", "http://google.com")
        node2 = TextNode("Testing text", "italic", "http://google.com")
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("Testing text", "bold", "http://google.com")
        node2 = TextNode("Testing text", "bold")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Testing text", "bold", "http://google.com")
        node2 = TextNode("Testing text", "bold", "http://google.com")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("Testing text yay!", "bold", "http://google.com")
        node2 = TextNode("Testing text", "bold", "http://google.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Testing text", "bold", "http://google.com")
        self.assertEqual("TextNode(Testing text, bold, http://google.com)", repr(node))

if __name__ == "__main__":
    unittest.main()