from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links,split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import os
import shutil
import re

def copy_contents(old_dir, new_dir):
    shutil.rmtree(new_dir)
    os.mkdir(new_dir)

    if not os.path.exists(old_dir):
        raise Exception("{old_dir} does not exist")
    if not os.path.exists(new_dir):
        raise Exception("{new_dir} does not exist")
    if old_dir == new_dir :
        raise Exception("Target directory is the same as source directory")
    
    dir_list = os.listdir(old_dir)

    for item in dir_list:
        item_path = old_dir + "/" + item 

        if os.path.isfile(item_path):
            shutil.copy(item_path, new_dir)
            print(f"Copying {item_path} to {new_dir}")
        elif os.path.isdir(item_path):
            item_path += "/"
            new_dir_path = new_dir + item + "/"
            os.mkdir(new_dir_path)
            print(f"Directory created at {new_dir_path}")
            copy_contents(item_path, new_dir_path)

def extract_title(markdown):
    match = re.search(r'^# (.+)', markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    raise Exception("Title not found")

def main():
    # old_dir = "/Users/mustakimfilumar/Documents/boots/github.com/MushisFil/StaticSiteGenerator/static/"
    # new_dir = "/Users/mustakimfilumar/Documents/boots/github.com/MushisFil/StaticSiteGenerator/public/"
    # copy_contents(old_dir, new_dir)

    md_doc = """## This is **bolded** paragraph

    This is another paragraph with *italic* text and `code` here
    This is the same paragraph on a new line

    * This is a list
    * with items

    # Hidden title hehe

    >You seem to be laboring under the delusion that I’m going to, what was the phrase, come quietly?
    >Well I can tell you this - I have no intention of going to Azkaban

    1. Order number 1
    2. Order number 2
    3. Order number 3

    ```print("HARRYDIDYOUPUTYOURNAMEINTHEGOBLETOFFIRE")```
    """

    print(extract_title(md_doc))


if __name__ == "__main__":
    main()
