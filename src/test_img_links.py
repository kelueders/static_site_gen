import unittest

from split_images_links import extract_markdown_images, extract_markdown_links, split_nodes_links, split_nodes_images
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

''' Testing split_nodes_images() '''

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
        actual = split_nodes_images([node])
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("kate hiking", TextType.IMAGE, "https://i.imgur.com/efasd.gif")
        ]
        self.assertEqual(expected, actual)

    def test_split_nodes_images_multi_node(self):
        node1 = TextNode("First there is an image ![eiffle tower](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        node2 = TextNode("Then there is another image ![kate hiking](https://i.imgur.com/efasd.gif)", TextType.TEXT)
        first = split_nodes_images([node1, node2])
        actual = split_nodes_images(first)
        expected = [
            TextNode("First there is an image ", TextType.TEXT),
            TextNode("eiffle tower", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("Then there is another image ", TextType.TEXT),
            TextNode("kate hiking", TextType.IMAGE, "https://i.imgur.com/efasd.gif")
        ]
        self.assertEqual(expected, actual)

class TestSplitNodesLinks(unittest.TestCase):
    def test_split_nodes_links_single(self):
        node = TextNode("This is text with a link [boot dev](https://boot.dev) and it's cool!", TextType.TEXT)
        actual = split_nodes_links([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("boot dev", TextType.LINK, "https://boot.dev"),
            TextNode(" and it's cool!", TextType.TEXT)
        ]
        self.assertEqual(expected, actual)