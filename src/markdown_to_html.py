from blocks_funcs import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode
from helpers import text_to_textnodes, text_node_to_html_node

def markdown_to_html_node(markdown):
    '''
    Converts a full markdown document into a single parent HTMLNode with child
    HTMLNode objects representing the nested elements.
    '''
    # Separate markdown document into blocks
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        # Determine block type
        block_type = block_to_block_type(block)

        # Based on the type of block, create a new HTMLNode with the proper data
        node = block_to_htmlnode(block, block_type)

        # If the block is a 'code' block, it does NOT do inline markdown parsing of its children
        if block_type != BlockType.CODE:

            # Split the value of the HTMLNode (a string) into a list of LeafNodes
            children = text_to_children(node.value)

            # Assign the children to the HTMLNode representing that block
            node.children = children
        
        else:
            pass



# HELPER FUNCTIONS
def strip_block_of_mdsyntax(block, block_type):
    if block_type == BlockType.HEADING or block_type == BlockType.QUOTE:
        return block.split(maxsplit = 1)[1]
    elif block_type == BlockType.CODE:
        return block.lstrip('`').rstrip('`')
    else:
        return block

def block_to_htmlnode(block, block_type):
    text = strip_block_of_mdsyntax(block, block_type)
    children = None

    if block_type == BlockType.PARAGRAPH:
        tag = 'p'

    elif block_type == BlockType.HEADING:
        tag = determine_heading_tag(block)

    elif block_type == BlockType.QUOTE:
        tag = 'blockquote'

    elif block_type == BlockType.CODE:
        return HTMLNode(tag = "pre", value = f"<code>{text}</code>")

    elif block_type == BlockType.UNORDERED_LIST:
        tag = "ul"
        children = get_list_children(block)

    elif block_type == BlockType.ORDERED_LIST:
        tag = "ol"
        children = get_list_children(block)

    return HTMLNode(tag = tag, value = text, children = children)

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
    children = [HTMLNode(tag = 'li', value = item) for item in items]
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

