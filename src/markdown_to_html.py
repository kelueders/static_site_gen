from blocks_funcs import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from helpers import text_to_textnodes, text_node_to_html_node
from textnode import TextNode
from textnode import TextType

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
        print(f"Block: {block}")
        # Determine block type
        block_type = block_to_block_type(block)

        # Based on the type of block, create a new HTMLNode (ParentNode) with the proper data

        # Generate the tag
        tag = get_block_tag(block, block_type)

        stripped_block = strip_block_of_mdsyntax(block, block_type)

        # Generate the children
        if block_type != BlockType.CODE:
            children = text_to_children(stripped_block)
        else:
            children = text_node_to_html_node(TextNode(stripped_block, TextType.CODE))

        parent_node = ParentNode(tag, children)

        # Add the newly created node to the list of new ParentNodes
        html_nodes.append(parent_node)

    return ParentNode("div", html_nodes)


# HELPER FUNCTIONS
def text_to_children(text):
    '''Takes a string of text and returns a list of LeafNodes that represent the inline markdown
    Works for all block types except CODE'''
    text_nodes = text_to_textnodes(text)

    children = []
    for node in text_nodes:
        child = text_node_to_html_node(node)
        children.append(child)

    return children

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

def determine_heading_tag(heading_block):
    '''
    Takes in a block of BlockType.HEADING and returns a node containing the proper 
    tag given the number of # characters.
    '''
    hash_marks = (heading_block.split(maxsplit = 1))[0]
    num_hash_marks = len(hash_marks)
    return f'h{num_hash_marks}'

def strip_block_of_mdsyntax(block, block_type):
    if block_type == BlockType.HEADING or block_type == BlockType.QUOTE:
        return block.split(maxsplit = 1)[1]
    elif block_type == BlockType.CODE:
        return block.strip('`\n')
    else:
        return block



