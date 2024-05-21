from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    tn = TextNode('Miaou Meow', 'bold', 'https://www.youtube.com/watch?v=QiVkKYw8Iao')
    #print(tn)

    leaf = LeafNode('p','This is a paragraph')
    # print(leaf.to_html())

    treecko = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    # print(treecko.to_html())

    node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
    )
    # <p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>
    # print(node.to_html())

    bulbasaur = TextNode("bulbasaur", "bold")
    leaf_bulba = text_node_to_html_node(bulbasaur)
    # print(leaf_bulba.to_html())

    chikorita = TextNode("chikorita", "link", "chikorita.com")
    # print(text_node_to_html_node(chikorita).to_html())

    ivysaur = TextNode("image of ivysaur", "image", "/url/to/img.png")
    # print(text_node_to_html_node(ivysaur).to_html())

    # node = TextNode("This is text with a `code block` word", "text")
    # new_nodes = split_nodes_delimiter([node], "`", "code")

    # nodee = TextNode("This is text with a `code block` word `code block2`", "text")
    # new_nodes = split_nodes_delimiter([nodee], "`", "code")
    # for node in new_nodes:
    #     print(node)

    # node2 = TextNode("`code block1` word `code block2`", "text")
    # new_nodes = split_nodes_delimiter([node2], "`", "text")

    # node22 = TextNode("`code block1` word `code block2` word2 `codeblock3`", "text")
    # new_nodes = split_nodes_delimiter([node22], "`", "code")
    # for node in new_nodes:
    #     print(node)

    # nodezero = TextNode("word word2", "text")
    # new_nodes = split_nodes_delimiter([nodezero], "`", "text")


    # node3 = TextNode("`code block`", "text")
    # new_nodes = split_nodes_delimiter([node3], "`", "text")

    text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
    extract_markdown_images(text)
    # [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]

    text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    print(extract_markdown_links(text))
    # [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]





if __name__ == "__main__":
    main()
