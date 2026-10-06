from ..data_struct import Node
from ..CONFIG import ref as REFERENCE

def clean(node: Node) -> Node:
    """
        Cleans Tree structure for better visualization and performance:
        **Rules**
        - 0 * a or 0 * x = None (Delete the node and its children entirely)
        - 1 * a or 1 * x = a or x (Collapse the Node)
        - 0 + a or 0 + x = a or x (Collapse the Node)
        - constant arithmetic: ^, *, /, +, -
        - *Will add more rules later.*
        
    """
    # Dealing with subchildren recursively:
    if node.left_node is not None:
         node.left_node = clean(node.left_node)
    if node.right_node is not None:
         node.right_node = clean(node.right_node)

    # Nothing to clean if this is a leaf:
    if node.left_node is None or node.right_node is None:
        return node

    # Cleaning current node (The node's children have NO subchildren now):
    term = '/=-4'
    if node.left_node.value not in REFERENCE['operator'].keys() and node.right_node.value not in REFERENCE['operator'].keys():  
        term = f"{node.left_node.value} {node.value} {node.right_node.value}"

    try:
        term_solution = eval(term)
        #print("CLEANING:", term, "=", term_solution)
        return Node(str(term_solution), dtype='base')

    except:
        if node.value == '*':
            if node.left_node.value in ['0', '0.0'] or node.right_node.value in ['0', '0.0']:
                return Node('0', 'base')

            if node.left_node.value == '1':
                return node.right_node

            if node.right_node.value == '1':
                return node.left_node


        elif node.value == '+':
            if node.left_node.value == '0':
                        return node.right_node
            
            if node.right_node.value == '0':
                return node.left_node

        return node # Will return identical node if no cleaning is to be done
