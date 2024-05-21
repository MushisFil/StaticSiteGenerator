import re
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, textnode):
        return self.text == textnode.text and self.text_type == textnode.text_type and self.url == textnode.url

    def __repr__(self):
        res = ""
        res += f'TextNode({self.text},{self.text_type}'
        if self.url is not None:
            res += f',{self.url})'
        else: res += ')'
        return res


def text_node_to_html_node(text_node):
    valid_types = {"text", "bold", "italic", "code", "link", "image"}
    if text_node.text_type not in valid_types:
        raise Exception("TextNode does not have a valid text type")
    
    if text_node.text_type == "text":
        return LeafNode(value = text_node.text)
    elif text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    elif text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    elif text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    elif text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt":text_node.text})
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
        else:
            splitted = node.text.split(delimiter)
            # print(splitted)
            # print(len(splitted))
            for i in range(len(splitted)):
                if (i%2 == 0) and (splitted[i] != ""):
                    new_nodes.append(TextNode(splitted[i], node.text_type, node.url)) # node.text_type should be text
                elif i%2 != 0:
                    new_nodes.append(TextNode(splitted[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
