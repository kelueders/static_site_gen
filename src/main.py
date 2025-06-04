from nodes.textnode import TextNode, TextType

def main():
    text_node1 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
    print(text_node1)

main()