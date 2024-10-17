import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    # def test_to_html_noprops(self):
    #     node = ParentNode("p", "This is a paragraph of text.")
    #     expected = '<p>This is a paragraph of text.</p>'
    #     self.assertEqual(expected, node.to_html())

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None,
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                                ],
                        )
            node.to_html()
    
    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()

    def test_4_children(self):
        node = ParentNode("p",
                          [
                            LeafNode("b", "Bold text"),
                            LeafNode(None, "Normal text"),
                            LeafNode("i", "italic text"),
                            LeafNode(None, "Normal text"),
                            ]
                    )
        expected = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(expected, node.to_html())

    def test_nested_child(self):
        node = ParentNode("ul",
                          [
                              ParentNode("li", [LeafNode("b", "Coffee")]),
                              LeafNode("li", "Tea"),
                              LeafNode("li", "Milk")
                            ]
                    )
        expected = '<ul><li><b>Coffee</b></li><li>Tea</li><li>Milk</li></ul>'
        self.assertEqual(expected, node.to_html())

if __name__ == "__main__":
    unittest.main()