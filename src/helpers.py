from textnode import TextType, TextNode
from leafnode import LeafNode

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
    new_nodes = []
    
    for node in old_nodes:
        # if an old node is not a TextType.TEXT type, add it to the new list as-is 
        #       (only split "text" type objects not bold, italic, etc.)
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        else:
            sentence_frags = node.text.split(delimiter)
            i = 0

            if len(sentence_frags) % 2 == 0:
                raise ValueError("That's invalid Markdown syntax. Formatted section not closed.")

            while i < len(sentence_frags):
                if i % 2 != 0:
                    new_node = TextNode(sentence_frags[i], text_type)
                    new_nodes.append(new_node)
                else:
                    new_node = TextNode(sentence_frags[i], TextType.TEXT)
                    new_nodes.append(new_node)
                i += 1

    return new_nodes

