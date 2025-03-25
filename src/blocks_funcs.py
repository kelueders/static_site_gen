from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown):
    '''
    Takes a raw Markdown string (representing a full document) as input.
    Returns a list of "block" strings.
    '''
    # Replace two new lines with any number of blank spaces between them with just '\n\n' next to eachother
    markdown = re.sub(r'\n\s*\n', '\n\n', markdown)

    # Split the text wherever there are two new lines
    blocks = markdown.split("\n\n")

    # Change all single new lines with any number of blank spaces after with just '\n'
    fixed_blocks = []
    for block in blocks:
        block = re.sub(r'\n\s*', '\n', block)
        fixed_blocks.append(block.strip())
        
    return fixed_blocks
    

def block_to_block_type(block):
    pass