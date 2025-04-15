from blocks_funcs import markdown_to_blocks, block_to_block_type

def markdown_to_html_node(markdown):
    '''
    Converts a full markdown document into a single parent HTMLNode
    '''
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)