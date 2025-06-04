from nodes.textnode import TextType, TextNode
from nodes.leafnode import LeafNode
from split_images_links import split_nodes_links, split_nodes_images

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
    potentially split into multiple nodes, of various types based on the delimiter.
    '''
    # Create an empty list to contain the result of ALL the old_nodes getting split up.
    new_nodes = []
    
    for node in old_nodes:
        # If an old node is not a TextType.TEXT type, add it to the new list as-is 
        #       (only split "text" type objects not bold, italic, etc.)       
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Create an empty list to contain the result of JUST the one node getting split up.
        split_nodes = []

        # Split the node up according to the provided delimiter.
        sentence_frags = node.text.split(delimiter)

        # If there is no matching delimiter (such as **bold ), then the syntax is invalid. Raise an error.
        if len(sentence_frags) % 2 == 0:
            raise ValueError("That's invalid Markdown syntax. Formatted section not closed.")

        # Iterate through the list of sentence fragments.
        for i in range(len(sentence_frags)):
            # If there is an empty fragment, move to the next item.
            if sentence_frags[i] == "":
                continue
            # If the fragment is an odd index, create a new node of the provided text_type.
            if i % 2 != 0:
                new_node = TextNode(sentence_frags[i], text_type)
                split_nodes.append(new_node)
            # If the fragment is an even index, create a new TEXT type node.
            else:
                new_node = TextNode(sentence_frags[i], TextType.TEXT)
                split_nodes.append(new_node)
        
        # Add these split nodes to the larger node list.
        new_nodes.extend(split_nodes)

    # Return the result of ALL the old_nodes getting split.
    return new_nodes


def text_to_textnodes(text):
    '''
    Uses the split_nodes_delimiter() function to split a string into separate TextNodes with TextTypes based on the delimiters.
    Also uses split_nodes_images() and split_nodes_links() to split on images and links

    Input: string of text
    Output: list of TextNodes of various text_types
    '''
    node = TextNode(text, TextType.TEXT)
    split_on_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    split_on_italics = split_nodes_delimiter(split_on_bold, "*", TextType.ITALIC)
    split_on_italics = split_nodes_delimiter(split_on_italics, "_", TextType.ITALIC)
    split_on_code = split_nodes_delimiter(split_on_italics, "`", TextType.CODE)
    split_on_images = split_nodes_images(split_on_code)
    final = split_nodes_links(split_on_images)

    return final

