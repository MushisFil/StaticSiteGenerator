import unittest

from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_different_text_type(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", "italic", "https://www.youtube.com/")
        self.assertEqual(node.__repr__(), 'TextNode(This is a text node,italic,https://www.youtube.com/)')

    def test_conversion(self):
        bulbasaur = TextNode("bulbasaur", "bold")
        leaf_bulba = text_node_to_html_node(bulbasaur)
        self.assertEqual(leaf_bulba.to_html(), '<b>bulbasaur</b>')
    
    def test_conversion2(self):
        ivysaur = TextNode("image of ivysaur", "image", "/url/to/img.png")
        res = '<img src="/url/to/img.png" alt="image of ivysaur"></img>'
        self.assertEqual(text_node_to_html_node(ivysaur).to_html(), res)
    
    def test_conversion3(self):
        chikorita = TextNode("chikorita", "link", "chikorita.com")
        res = '<a href="chikorita.com">chikorita</a>'
        self.assertEqual(text_node_to_html_node(chikorita).to_html(), res)
    
    def test_conversion4(self):
        invalid_type = TextNode("nothing", "please")
        with self.assertRaises(Exception):
            text_node_to_html_node(invalid_type)

    def test_split_delimiter(self):
        node22 = TextNode("`code block1` word `code block2` word2 `codeblock3`", "text")
        new_nodes = split_nodes_delimiter([node22], "`", "code")
        expected = [
            TextNode("code block1", "code"),
            TextNode(" word ", "text"),
            TextNode("code block2", "code"),
            TextNode(" word2 ", "text"),
            TextNode("codeblock3", "code")
        ]
        allTrue = 1
        for i in range(len(new_nodes)):
            if new_nodes[i] != expected[i]:
                allTrue = 0
        self.assertEqual(allTrue, 1)
    
    def test_split_delimiter2(self):
        node = TextNode("normal text **bold text** normal text", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        expected = [
            TextNode("normal text ", "text"),
            TextNode("bold text", "bold"),
            TextNode(" normal text", "text"),
        ]
        allTrue = 1
        for i in range(len(new_nodes)):
            if new_nodes[i] != expected[i]:
                allTrue = 0
        self.assertEqual(allTrue, 1)
    
    def test_split_nodes_image1(self):
        node = TextNode("![1st image](https://image1.png) text in between ![2nd image](https://image2.png)![3rd image](https://image3.png) text at the end","text")
        obtained = split_nodes_image([node])
        expected = [
            TextNode("1st image", "image", "https://image1.png"),
            TextNode(" text in between ", "text"),
            TextNode("2nd image", "image", "https://image2.png"),
            TextNode("3rd image", "image", "https://image3.png"),
            TextNode(" text at the end", "text")
        ]
        all_equal = 1
        for i in range(len(expected)):
            if expected[i] != obtained[i]:
                all_equal = 0
        if len(expected) != len(obtained): all_equal = 0
        self.assertEqual(all_equal, 1)
    
    def test_split_nodes_image2(self):
        node = TextNode("![1st image](https://image1.png)![2nd image](https://image2.png)![3rd image](https://image3.png)","text")
        obtained = split_nodes_image([node])
        expected = [
            TextNode("1st image", "image", "https://image1.png"),
            TextNode("2nd image", "image", "https://image2.png"),
            TextNode("3rd image", "image", "https://image3.png")
        ]
        all_equal = 1
        for i in range(len(expected)):
            if expected[i] != obtained[i]:
                all_equal = 0
        if len(expected) != len(obtained): all_equal = 0
        self.assertEqual(all_equal, 1)
    
    def test_split_nodes_image3(self):
        node = TextNode("simply text","text")
        obtained = split_nodes_image([node])
        expected = [
            TextNode("simply text", "text")
        ]
        all_equal = 1
        for i in range(len(expected)):
            if expected[i] != obtained[i]:
                all_equal = 0
        if len(expected) != len(obtained): all_equal = 0
        self.assertEqual(all_equal, 1)
    
    def test_split_nodes_link(self):
        node = TextNode("[1st link](https://link1.com) text in between [2nd link](https://link2.com)[3rd link](https://link3.com) text at the end","text")
        obtained = split_nodes_link([node])
        expected = [
            TextNode("1st link", "link", "https://link1.com"),
            TextNode(" text in between ", "text"),
            TextNode("2nd link", "link", "https://link2.com"),
            TextNode("3rd link", "link", "https://link3.com"),
            TextNode(" text at the end", "text")
        ]
        all_equal = 1
        for i in range(len(expected)):
            if expected[i] != obtained[i]:
                all_equal = 0
        if len(expected) != len(obtained): 
            all_equal = 0
        # print("*********Expected***********")
        # for node in expected:
        #     print(node)
        # print("*********Obtained***********")
        # for node in obtained:
        #     print(node)
        # print("********************")
        
        self.assertEqual(all_equal, 1)



if __name__ == "__main__":
    unittest.main()
