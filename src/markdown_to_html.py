from blocks_funcs import markdown_to_blocks, block_to_block_type, BlockType
from nodes.htmlnode import HTMLNode
from nodes.parentnode import ParentNode
from nodes.leafnode import LeafNode
from helpers import text_to_textnodes, text_node_to_html_node
from nodes.textnode import TextNode
from nodes.textnode import TextType

def markdown_to_html_node(markdown):
    '''
    Converts a full markdown document into a single parent HTMLNode with child (Leaf)
    HTMLNode objects representing the nested elements.
    '''
    # Create empty list to hold the list of HTMLNodes corresponding to each block in the markdown doc
    html_nodes = []

    # Separate markdown document into blocks
    blocks = markdown_to_blocks(markdown)

    print(f'Number of blocks: {len(blocks)}')

    for block in blocks:

        print(f"Block: {block}")

        # Determine block type
        block_type = block_to_block_type(block)

        # print(f"Block Type: {block_type}")


        # Based on the type of block, create a new HTMLNode (ParentNode) with the proper data

        # Generate the tag
        tag = get_block_tag(block, block_type)

        stripped_block = strip_block_of_mdsyntax(block, block_type)

        # Generate the children
        if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
            leafs = get_list_children(block, block_type)
            return li_convert_nodes(leafs)
        
        elif block_type != BlockType.CODE:
            children = text_to_children(stripped_block)
            if children == 0:
                node = LeafNode(tag, stripped_block)
            else:
                node = ParentNode(tag, children)
                
        else:
            pre_tag = tag[0]
            code_node = text_node_to_html_node(TextNode(stripped_block, TextType.CODE))
            node = ParentNode(pre_tag, [code_node])

        # Add the newly created node to the list of new nodes
        html_nodes.append(node)

    print(f"HTML NODE LIST: {html_nodes}")

    return ParentNode("div", html_nodes)


# HELPER FUNCTIONS
def text_to_children(text):
    '''Takes a string of text and returns a list of LeafNodes that represent 
    the inline markdown.
    Note: Works for all block types except CODE'''
    children = []
    text_nodes = text_to_textnodes(text)

    for node in text_nodes:
        child = text_node_to_html_node(node)
        children.append(child)
    
    if len(children) == 1:
        return 0

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
        return ("pre", "code")

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
        # return block.strip('`').lstrip('\n')
    else:
        return block
    
def get_list_children(list_block, block_type):
    '''
    Takes in a block of type UNORDERED_LIST or ORDERED_LIST and returns a 
    list of HTMLNode objects containing each list item.
    '''
    items = list_block.split('\n')

    for item in items:
        if block_type == BlockType.UNORDERED_LIST:
            return [LeafNode(tag = 'li', value = item[2:]) for item in items]
        else:
            return [LeafNode(tag = 'li', value = item[3:]) for item in items]
        
# def determine_if_parent(children):
#     '''
#     Input: array of children
#     Output: boolean value where True means the node should be a Parent, False means it should be a Leaf
#     '''
#     # If there is inline markdown, the children list will be a list longer than length of 1.
#     if len(children) > 1:
#         return True
#     return False

def li_convert_nodes(leaf_nodes):
    '''
    Takes in a list of LeafNodes. If the value of the node contains inline markdown,
    then that list item is converted to a ParentNode with the inline parts as children.
    Returns a new list of HTMLNodes that are either Leafs or Parents.
    Notes: uses text_to_children()
    '''
    list_items = []
    for node in leaf_nodes:
        if text_to_children(node.value) == 0:
            list_items.append(node)
        else:
            new_parent = ParentNode(node.tag, text_to_children(node.value))
            list_items.append(new_parent)
    return list_items

