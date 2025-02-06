from textnode import TextType, TextNode
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT.value:
        leaf = LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD.value:
        leaf = LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC.value:
        leaf = LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE.value:
        leaf = LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK.value:
        leaf = LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE.value:
        leaf = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise AttributeError(f"invalid text type: {text_node.text_type}")
    
    return leaf

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    '''
    Takes a list of "old notes", a delimiter, and a text type and returns
    a new list of nodes, where any "text" type nodes in the input list are
    potentially split into multiple nodes based on the syntax.
    '''
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)

        sentence_frags = node.text.split(delimiter)

        for sentence in sentence_frags:
            new_node = TextNode(sentence, text_type)
            new_nodes.append(new_node)

    return new_nodes
