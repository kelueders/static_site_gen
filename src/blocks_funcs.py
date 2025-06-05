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

    # Replace all single new lines with any number of blank spaces after with just '\n'
    fixed_blocks = []
    for block in blocks:
        block = re.sub(r'\n\s*', '\n', block)
        fixed_blocks.append(block.strip())
        
    return fixed_blocks
    

def block_to_block_type(block):
    '''
    Takes a block and returns the BlockType of the block.
    '''
    if re.search(r'^#{1,6}', block):
        return BlockType.HEADING
    
    elif re.search(r'^```[\s\S]*```$', block):
        return BlockType.CODE
    
    elif re.search(r'^>.*(\n>.*)+$', block):
        return BlockType.QUOTE
    
    elif re.search(r'^- .*(\n- .*)+$', block):
        return BlockType.UNORDERED_LIST
    
    elif re.search(r'\d\.', block):
        num_list = block.split("\n")
        num = 1

        for item in num_list:
            if re.search(fr'{num}\. .*', item):
                num += 1
            else:
                break

        if num == len(num_list) + 1:
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    
    else:
        return BlockType.PARAGRAPH
        
    