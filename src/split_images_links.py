import re
import logging

from textnode import TextNode, TextType

logging.basicConfig(filename="app.log", level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def extract_markdown_images(text):
    '''
    Takes raw markdown text and returns a list of tuples. Each
    tuple contains the alt text and the URL of the image.
    image_tuples = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    '''
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    '''
    Takes raw markdown text and returns a list of tuples. Each tuple
    contains the anchor text and the URL.
    link_tuples = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    '''
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_images(old_nodes):
    '''
    Takes a list of TextNodes and returns a new list of TextNodes
    that separates the images content into separate nodes from the text.
    '''
    logger = logging.getLogger(__name__)

    new_nodes = []

    for j, node in enumerate(old_nodes):
        logger.debug(f'  Node #{j}:  {node}')

        image_tuples = extract_markdown_images(node.text)
        logger.debug(f'image_tuples = {image_tuples}')

        if not image_tuples:
            new_nodes.append(node)
            continue

        sections = []

        for i in range(len(image_tuples)):
            img_alt = image_tuples[i][0]
            img_link = image_tuples[i][1]
            sections.extend(node.text.split(f"![{img_alt}]({img_link})", 1))

        logger.debug(f'sections = {sections}')

        first_text = sections[0]
        second_text = sections[1]

        new_node = [
            TextNode(first_text, TextType.TEXT),
            TextNode(img_alt, TextType.IMAGE, img_link),
            TextNode(second_text, TextType.TEXT)
        ]
        

        logger.debug(f'new_node = {new_node}')
        logger.debug(f'')

        new_nodes.extend(new_node)

    return new_nodes

def split_nodes_link(old_nodes):
    pass