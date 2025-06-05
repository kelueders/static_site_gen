from nodes.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props) # A ParentNode has no value

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: No tag was given")
        elif self.children is None:
            raise ValueError("Invalid parent HTML: No children were given")
        else:
            result = ""
            for child in self.children:
                result += child.to_html()

            return f'<{self.tag}>{result}</{self.tag}>'
        
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
