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
    new_nodes = []

    for j, node in enumerate(old_nodes):

        image_tuples = extract_markdown_images(node.text)

        if not image_tuples:
            new_nodes.append(node)
            continue

        sections = []

        text_assess = node.text

        for img_alt, img_link in image_tuples:
            split_text = text_assess.split(f"![{img_alt}]({img_link})", 1)
            sections.append(split_text[0])
            text_assess = split_text[1] if len(split_text) > 1 else ""

        if text_assess:
            sections.append(text_assess)

        # sections now contains just the text content, split into a list, no image information
        # image_tuples contains a list of the image information
        # put it together into a single list using pointers to avoid an IndexError

        sections_images = []
        p1 = 0
        p2 = 0
        while len(sections_images) < len(sections) + len(image_tuples):
            if len(sections_images) % 2 == 0:
                sections_images.append(sections[p1])
                p1 += 1
            else:
                sections_images.append(image_tuples[p2])
                p2 += 1

        for x in range(len(sections_images)):
            if x % 2 == 0:
                new_nodes.append(TextNode(sections_images[x], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections_images[x][0], TextType.IMAGE, sections_images[x][1]))

    return new_nodes

def split_nodes_links(old_nodes):
    '''
    Takes a list of TextNodes and returns a new list of TextNodes
    that separates the links content into separate nodes from the text.
    '''
    logger = logging.getLogger(__name__)
    new_nodes = []
    
    for j, node in enumerate(old_nodes):
        logger.debug(f'  Node #{j}:  {node}')

        link_tuples = extract_markdown_links(node.text)
        logger.debug(f'link_tuples = {link_tuples}')

        if not link_tuples:
            new_nodes.append(node)
            continue

        sections = []

        text_assess = node.text

        for link_alt, link_link in link_tuples:
            split_text = text_assess.split(f"[{link_alt}]({link_link})", 1)
            sections.append(split_text[0])
            text_assess = split_text[1] if len(split_text) > 1 else ""

        if text_assess:
            sections.append(text_assess)

        logger.debug(f'sections = {sections}')
        logger.debug(f'link_tuples = {link_tuples}')

        # sections now contains just the text content, split into a list, no link information
        # link_tuples contains a list of the link information
        # put it together into a single list using pointers to avoid an IndexError

        sections_links = []
        p1 = 0
        p2 = 0
        while len(sections_links) < len(sections) + len(link_tuples):
            if len(sections_links) % 2 == 0:
                sections_links.append(sections[p1])
                p1 += 1
            else:
                sections_links.append(link_tuples[p2])
                p2 += 1

        logger.debug(f"sections_links = {sections_links}")

        for x in range(len(sections_links)):
            if x % 2 == 0:
                new_nodes.append(TextNode(sections_links[x], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections_links[x][0], TextType.LINK, sections_links[x][1]))

        logger.debug(f"new_nodes: {new_nodes}")
        logger.debug(f'')

    return new_nodes