class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag            # string - "p" or "a"
        self.value = value        # string - text inside
        self.children = children  # list - of HTMLNode objects
        self.props = props        # dict - attributes of HTML tag

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
    
    def to_html(self):
        raise NotImplementedError("to_html is not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for k, v in self.props.items():
            props_html += f' {k}="{v}"'
        return props_html
    


