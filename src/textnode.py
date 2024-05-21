import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from blockvars import *

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted = extract_markdown_images(node.text)

        if len(extracted) == 0 and node.text != "": # no images found
            new_nodes.append(node)
        else:
            # found at least one image
            curr_length = None
            for i in range(len(extracted)):
                image_tup = extracted[i]
                splitted = node.text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                if i == 0:
                    if splitted[0] != "":
                        new_nodes.append(TextNode(splitted[0], "text"))
                    new_nodes.append(TextNode(image_tup[0], "image", image_tup[1]))
                    curr_length = len(splitted[0]) + len(image_tup[0]) + len(image_tup[1]) + 5
                else:
                    nodes_to_be_added, curr_length, splitted = helper(extracted, node, i, curr_length, func_type = "image")
                    new_nodes.extend(nodes_to_be_added)
                if (i == len(extracted) - 1) and splitted[len(splitted)-1] != "":
                    new_nodes.append(TextNode(splitted[len(splitted)-1], "text"))
    return new_nodes


def helper(extracted, node, i, length_prev, func_type = "image"):
    image_tup = extracted[i]
    if func_type == "image":
        splitted = node.text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
    else:
        splitted = node.text.split(f"[{image_tup[0]}]({image_tup[1]})", 1)
    new_nodes = []
    before_image_text = splitted[0][length_prev:]
    if before_image_text != "":
        new_nodes.append(TextNode(before_image_text, "text"))
    new_nodes.append(TextNode(image_tup[0], func_type, image_tup[1]))
    curr_length = length_prev + len(before_image_text) + len(image_tup[0]) + len(image_tup[1]) + 4
    if func_type == "image":
        curr_length += 1

    return new_nodes, curr_length, splitted
    

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted = extract_markdown_links(node.text)
        # print(extracted)

        if len(extracted) == 0 and node.text != "": # no images found
            new_nodes.append(node)
        else:
            # found at least one link
            curr_length = None
            for i in range(len(extracted)):
                image_tup = extracted[i]
                splitted = node.text.split(f"[{image_tup[0]}]({image_tup[1]})", 1)
                if i == 0:
                    if splitted[0] != "":
                        new_nodes.append(TextNode(splitted[0], "text"))
                    new_nodes.append(TextNode(image_tup[0], "link", image_tup[1]))
                    curr_length = len(splitted[0]) + len(image_tup[0]) + len(image_tup[1]) + 4
                else:
                    nodes_to_be_added, curr_length, splitted = helper(extracted, node, i, curr_length, func_type = "link")
                    new_nodes.extend(nodes_to_be_added)
                if (i == len(extracted) - 1) and splitted[len(splitted)-1] != "":
                    new_nodes.append(TextNode(splitted[len(splitted)-1], "text"))
    return new_nodes


def text_to_textnodes(text):
    tempNode = TextNode(text, "text")
    bolded = split_nodes_delimiter([tempNode], "**", "bold")
    coded = split_nodes_delimiter(bolded, "`", "code")
    italicized = split_nodes_delimiter(coded, "*", "italic")
    imaged = split_nodes_image(italicized)
    linked = split_nodes_link(imaged)
    return linked

def markdown_to_blocks(markdown):
    # First Blocks
    fun = lambda x : x.lstrip(' ')
    fun2 = lambda x: True if x != "" else False
    blocks = list(map(fun, markdown.split('\n\n')))
    filtered = list(filter(fun2, blocks))

    # Then on each line
    new_blocks = []
    for block in blocks:
        lines = list(map(fun, block.split('\n')))
        lines_filtered = list(filter(fun2, lines))
        new_blocks.append('\n'.join(lines_filtered))
    
    # print(filtered)
    # print('\n\n'.join(new_blocks))
    return new_blocks

# A function that checks whether ever first character of each element in the list starts
# with the same character c
def inspect_lines(lines, c, index):
    for line in lines:
        if line[index] != c:
            return 0
    return 1

def check_ordered_list(lines):
    pattern = r'^(\d+)\. .+'
    previous_number = 0

    for line in lines:
        match = re.match(pattern, line)
        if not match:
            return False
        curr_num = int(match.group(1))
        if curr_num != previous_number + 1:
            return False
        previous_number = curr_num 
    
    return True




def block_to_block_type(block):

    if block[0] == "#":
        return block_type_heading
    elif block[0:3] == '```' and block[len(block)-3 : len(block)] == '```':
        return block_type_code
    else:
        lines = block.split('\n')
        if inspect_lines(lines, '>', 0):
            return block_type_quote
        elif (inspect_lines(lines, '*', 0) or inspect_lines(lines, '-', 0)) and inspect_lines(lines, ' ', 1):
            return block_type_unordered_list
        elif check_ordered_list(lines):
            return block_type_ordered_list
    return block_type_paragraph
        
