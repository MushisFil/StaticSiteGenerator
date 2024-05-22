from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links,split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from blockvars import *
import os
import shutil
import re

def copy_contents(old_dir, new_dir):
    shutil.rmtree(new_dir)
    os.mkdir(new_dir)

    if not os.path.exists(old_dir):
        raise Exception(f"{old_dir} does not exist")
    if not os.path.exists(new_dir):
        raise Exception(f"{new_dir} does not exist")
    if old_dir == new_dir :
        raise Exception(f"Target directory is the same as source directory")
    
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
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == block_type_heading:
            for line in block.split('\n'):
                match = re.match(r'^# (.+)', line)
                if match:
                    return match.group(1).strip()
        
    match = re.search(r'^# (.+)', markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    raise Exception("Title not found")

def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise Exception(f"{from_path} does not exist")
    if not os.path.exists(template_path):
        raise Exception(f"{template_path} does not exist")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    with open(from_path) as f:
        markdown = f.read()
    # print(markdown)
    with open(template_path) as f:
        template = f.read()
    
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)

    splitted = from_path.split('/')
    filename = splitted[len(splitted)-1].split('.')[0]
    
    html_path = dest_path + filename + '.html'
    with open(html_path, 'w') as f:
        f.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception(f"{dir_path_content} does not exist")
    if not os.path.exists(template_path):
        raise Exception(f"{template_path} does not exist")
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    
    items = os.listdir(dir_path_content)
    for item in items:
        item_path = dir_path_content + item
        if os.path.isfile(item_path):
            splitted =  item.split('.')
            # print(splitted)
            if splitted[1] == 'md':
                from_path = dir_path_content + item 
                generate_page(from_path, template_path, dest_dir_path)
        elif os.path.isdir(item_path):
            new_from_path = dir_path_content + item + "/"
            new_to_path = dest_dir_path + item + "/"
            # print("***********")
            # print(new_from_path)
            # print("***********")
            # print(new_to_path)
            generate_pages_recursive(new_from_path, template_path, new_to_path)




def main():
    old_dir = "/Users/mustakimfilumar/Documents/boots/github.com/MushisFil/StaticSiteGenerator/static/"
    new_dir = "/Users/mustakimfilumar/Documents/boots/github.com/MushisFil/StaticSiteGenerator/public/"
    copy_contents(old_dir, new_dir)
    # generate_page('/Users/mustakimfilumar/Documents/boots/github.com/MushisFil/StaticSiteGenerator/static/doc.md', 0, 0)
    from_path = '/Users/mustakimfilumar/Documents/boots/github.com/MushisFil/StaticSiteGenerator/content/index.md'
    dest_path =  '/Users/mustakimfilumar/Documents/boots/github.com/MushisFil/StaticSiteGenerator/public/'
    template_path = '/Users/mustakimfilumar/Documents/boots/github.com/MushisFil/StaticSiteGenerator/template.html'
    dir_path_content = '/Users/mustakimfilumar/Documents/boots/github.com/MushisFil/StaticSiteGenerator/content/'
    # generate_page(from_path, template_path, dest_path)
    generate_pages_recursive(dir_path_content, template_path, dest_path)



if __name__ == "__main__":
    main()
