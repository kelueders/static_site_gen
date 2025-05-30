from blocks_funcs import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from helpers import text_to_textnodes, text_node_to_html_node
from textnode import TextNode

def markdown_to_html_node(markdown):
    '''
    Converts a full markdown document into a single parent HTMLNode with child (Leaf)
    HTMLNode objects representing the nested elements.
    '''
    # Create empty list to hold the list of HTMLNodes corresponding to each block in the markdown doc
    html_nodes = []

    # Separate markdown document into blocks
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        # Determine block type
        block_type = block_to_block_type(block)

        # Based on the type of block, create a new HTMLNode with the proper data
        node = block_to_htmlnode(block, block_type)

        # If the block is not a 'code' block, do inline markdown parsing of its children
        # 'code' blocks do not do inline markdown parsing
        if block_type != BlockType.CODE:
            # Split the value of the HTMLNode (a string) into a list of LeafNodes
            children = text_to_children(node.value)

            # Assign the children to the HTMLNode representing that block
            node.children = children

        # Append the node to the list of HTMLNodes corresponding to each block
        html_nodes.append(node)

    return ParentNode("div", html_nodes)

# HELPER FUNCTIONS
def strip_block_of_mdsyntax(block, block_type):
    if block_type == BlockType.HEADING or block_type == BlockType.QUOTE:
        return block.split(maxsplit = 1)[1]
    elif block_type == BlockType.CODE:
        new1 = block.replace("\n", "")
        new2 = new1.lstrip('`').rstrip('`')
        return new2.replace("\n", "")
    else:
        return block
    
def get_block_tag(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        tag = 'p'

    elif block_type == BlockType.HEADING:
        tag = determine_heading_tag(block)

    elif block_type == BlockType.QUOTE:
        tag = 'blockquote'

    elif block_type == BlockType.UNORDERED_LIST:
        tag = "ul"

    elif block_type == BlockType.ORDERED_LIST:
        tag = "ol"
    
    elif block_type == BlockType.CODE:
        tag = "code"

    return tag

# def block_to_htmlnode(block, block_type):
#     text = strip_block_of_mdsyntax(block, block_type)

#     tag = get_block_tag(block, block_type)

#     if block_type == BlockType.CODE:
#         leaf = LeafNode(tag = tag, value = text)
#         return ParentNode(tag = "pre", children = [leaf])

#     children = text_to_children(text)

#     if determine_if_parent(children):
#         if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
#             list_children = get_list_children(block)
#             for child in list_children:
#                 if determine_if_parent(child):
#                     pass
#             return ParentNode(tag = tag, )
#         return ParentNode(tag = tag, children = children)

#     return HTMLNode(tag = tag, value = text, children = children)

# def determine_if_parent(children):
#     '''
#     Input: array of children
#     Output: boolean value where True means the node should be a Parent, False means it should be a Leaf
#     '''
#     # If there is inline markdown, the children list will be a list longer than length of 1.
#     if len(children) > 1:
#         return True
#     return False

def determine_heading_tag(heading_block):
    '''
    Takes in a block of BlockType.HEADING and returns a node containing the proper 
    tag given the number of # characters.
    '''
    hash_marks = (heading_block.split(maxsplit = 1))[0]
    num_hash_marks = len(hash_marks)
    return f'h{num_hash_marks}'

def get_list_children(list_block):
    '''
    Takes in a block of type UNORDERED_LIST or ORDERED_LIST and returns a 
    list of HTMLNode objects containing each list item.
    '''
    items = list_block.split('\n')
    children = [LeafNode(tag = 'li', value = item) for item in items]
    return children

def text_to_children(text):
    '''
    Takes a string of text
    Returns a list of LeafNodes that represent the inline markdown
    '''
    # Split the text into a separate list of TextNodes of different text_types
    textnode_list = text_to_textnodes(text)

    # Convert the list of TextNodes to a list of LeafNodes and return the result
    return [text_node_to_html_node(node) for node in textnode_list]