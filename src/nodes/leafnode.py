from nodes.htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props) # A LeafNode has no children
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"
    
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
            self.tag == other.tag 
            and self.value == other.value 
            and self.props == other.props
        )

    def to_html(self):
        if not self.value:
            raise ValueError('Invalid HTML: All leaf nodes must have a value')
        elif not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
