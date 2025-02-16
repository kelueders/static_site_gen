import logging

from textnode import TextType, TextNode
from leafnode import LeafNode

logging.basicConfig(filename="app.log", level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def text_node_to_html_node(text_node):
    '''
    Takes a TextNode and converts it to a LeafNode 
    '''
    if text_node.text_type == TextType.TEXT:
        leaf = LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        leaf = LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        leaf = LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        leaf = LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        leaf = LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        leaf = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise AttributeError(f"invalid text type: {text_node.text_type}")
    
    return leaf

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    '''
    Takes a list of "old nodes", a delimiter, and a text type and returns
    a new list of nodes, where any "text" type nodes in the input list are
    potentially split into multiple nodes based on the syntax.
    '''
    logger = logging.getLogger(__name__)

    new_nodes = []
    
    for node in old_nodes:
        # if an old node is not a TextType.TEXT type, add it to the new list as-is 
        #       (only split "text" type objects not bold, italic, etc.)
        logger.debug(f'  Node:  {node}')
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

            logger.debug(f"node.text_type: {node.text_type}, type: {type(node.text_type)}")
            logger.debug(f"TextType.TEXT: {TextType.TEXT}, type: {type(TextType.TEXT)}")
        else:
            sentence_frags = node.text.split(delimiter)
            i = 0
            logger.debug(f'Sentences split into an array: {sentence_frags}')

            if len(sentence_frags) % 2 == 0:
                raise Exception("That's invalid Markdown syntax.")

            while i < len(sentence_frags):
                if i % 2 != 0:
                    if delimiter == "`":
                        new_node = TextNode(sentence_frags[i], TextType.CODE)
                        new_nodes.append(new_node)
                    elif delimiter == "**":
                        new_node = TextNode(sentence_frags[i], TextType.BOLD)
                        new_nodes.append(new_node)
                    elif delimiter == "*":
                        new_node = TextNode(sentence_frags[i], TextType.ITALIC)
                        new_nodes.append(new_node)
                else:
                    new_node = TextNode(sentence_frags[i], TextType.TEXT)
                    new_nodes.append(new_node)
                i += 1
    logger.debug("")

    return new_nodes

