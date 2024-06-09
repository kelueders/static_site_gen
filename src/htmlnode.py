class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag            # string - "p" or "a"
        self.value = value        # string - text inside
        self.children = children  # list - of HTMLNode objects
        self.props = props        # dict - attributes of HTML tag

    def __repr__(self):
        return f"HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})"
    
    def to_html(self):
        raise NotImplementedError("This is not implemented")
    
    def props_to_html(self):
        html = ""
        for k, v in self.props.items():
            html += f' {k}="{v}"'
        return html
    
    
