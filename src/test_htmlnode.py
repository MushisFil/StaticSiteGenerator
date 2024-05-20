import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode("a", "Link to Youtube", None, {"href": "https://www.youtube.com"})
        self.assertEqual(node.tag, "a")
    
    def test_repr(self):
        node = HTMLNode("a", "Link to Youtube", None, {"href": "https://www.youtube.com"})
        self.assertEqual(node.__repr__(), "HTMLNode(a, Link to Youtube, None, {'href': 'https://www.youtube.com'})")

    def test_leaf_value(self):
        node = LeafNode('p','This is a paragraph')
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")
    
    def test_leaf_props(self):
        treecko = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(treecko.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_multiple_props(self):
        treecko = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(treecko.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')
    
    def test_parentNode_output(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        res = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), res)
    
    def test_parentNode_no_children(self):
        node = ParentNode("p",[],)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parent_as_child(self):
        parent = ParentNode(
            "h",
            [LeafNode("b", "Text in bold")])
        
        node = ParentNode(
            "p",
            [
                LeafNode("i", "Text in italic"),
                parent
            ]
        )
        res = '<p><i>Text in italic</i><h><b>Text in bold</b></h></p>'
        self.assertEqual(node.to_html(),res)


if __name__ == "__main__":
    unittest.main()
