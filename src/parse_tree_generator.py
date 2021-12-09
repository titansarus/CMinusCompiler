from anytree import Node, RenderTree
from cminus_parser import ParseNode

def get_tree(node: ParseNode, parent: ParseNode = None):
    root = Node(node.get_name(), parent=parent)
    for child in node.children:
        get_tree(child, root)
    return root

def render_tree(tree):
    result = ""
    for pre, fill, node in RenderTree(tree):
        result += f'{pre}{node.name}\n'
    return result