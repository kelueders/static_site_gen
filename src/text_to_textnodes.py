from helpers import split_nodes_delimiter
from split_images_links import split_nodes_links, split_nodes_images
from textnode import TextType, TextNode

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    split_on_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    split_on_italics = split_nodes_delimiter(split_on_bold, "*", TextType.ITALIC)
    split_on_code = split_nodes_delimiter(split_on_italics, "`", TextType.CODE)
    split_on_images = split_nodes_images(split_on_code)
    final = split_nodes_links(split_on_images)

    return final