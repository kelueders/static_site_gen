from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    '''
    Represents different types of inline text that can exist in HTML and Markdown
    '''
    def __init__(self, text, text_type, url = None):
        self.text = text                    # string - the content
        self.text_type = text_type          # enum
        self.url = url                      # string - the link (optional) (for images and links)

    def __eq__(self, other):
        return (
            self.text == other.text 
            and self.text_type == other.text_type 
            and self.url == other.url
        )
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


