from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, props)
        self.value = value

    def to_html(self):
        if not self.value:
            raise ValueError('No value, all leaf nodes must have a value')
        elif not self.tag:
            return f"{self.value}"
        elif not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            props_html = self.props_to_html()
            print(props_html)
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"