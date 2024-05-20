class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        res = ""
        for key, value in self.props.items():
            res+= f' {key}="{value}"'
        return res
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        if value is None:
            raise ValueError("All leaf nodes require a value")
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.tag is None:
            return self.value
        else:
            res = f'<{self.tag}'
            if self.props != None:
                res += self.props_to_html()
            res += f">{self.value}</{self.tag}>"
        return res


class ParentNode(HTMLNode):
    def __init__(self, tag = None, children = None, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag was not provided")
        if self.children is None or not self.children:
            raise ValueError("Children were not provided")
        res = f"<{self.tag}>"
        for child in self.children:
            res += child.to_html()
        res += f"</{self.tag}>"
        return res
        

    

        

