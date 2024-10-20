from textnode import TextType
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
        raise TypeError("This text has the wrong type.")
    
    return leaf