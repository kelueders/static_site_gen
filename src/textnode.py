class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text             # string - the content
        self.text_type = text_type   # string - bold, italic, etc.
        self.url = url               # string - the link (optional)

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


