import unittest

from split_images_links import extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_link
from textnode import TextNode, TextType

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

class TestSplitNodesImages(unittest.TestCase):
    def test_split_nodes_images_single(self):
        node = TextNode("This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and it's cool!", TextType.TEXT)
        actual = split_nodes_images([node])
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and it's cool!", TextType.TEXT)
        ]
        self.assertEqual(expected, actual)

    def test_split_nodes_images_no_image(self):
        node = TextNode("There is no image in this text.", TextType.TEXT)
        actual = split_nodes_images([node])
        expected = [
            TextNode("There is no image in this text.", TextType.TEXT)
        ]
        self.assertEqual(expected, actual)

    def test_split_nodes_images_double(self):
        node = TextNode("This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![kate hiking](https://i.imgur.com/efasd.gif)", TextType.TEXT)
        first = split_nodes_images([node])
        second = split_nodes_images(first)
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("kate hiking", TextType.IMAGE, "https://i.imgur.com/efasd.gif")
        ]
        self.assertEqual(expected, second)