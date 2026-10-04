from .data_struct import Tree, Node

def visualize_tree(tree: Tree):
    if tree.master_node is not None:
        visualize_node(tree.master_node)

def visualize_node(node: Node, prefix=''):
    "Prints the node and its children only. To be used recursively."
    print(prefix + str(node.value)) # Parent Node

    if node.left_node:
        print(prefix + "├── ", end="")
        visualize_node(node.left_node, prefix + "│   ")

    if node.right_node:
        print(prefix + "└── ", end="")
        visualize_node(node.right_node, prefix + "    ")

    