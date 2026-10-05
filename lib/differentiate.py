from .data_struct import Node
from . import derivatives

from . import parsing

def Differentiate(root_node: Node, var: str) -> Node:
    """
    - `root_node`: The root node of a term.
    - `var`: Variable to whose respect differentiation is to be done.
    """
    diff_ptr = root_node # Differential Pointer

    root_val = root_node.value
    
    # Basic operations:
    if root_val == '^':
        base = root_node.left_node.value
        pow = root_node.right_node.value

        if base == var: # x ^ n
            #print("Case 1.")
            return parsing.CreateTree(derivatives.power_of_var(base, pow)) # Returns Node
        
        elif base == 'e' and pow == var: # e ^ n
            return parsing.CreateTree(derivatives.e_of_var(pow)) # Returns Node

        elif base != 'e' and pow == var: # a ^ x (TODO later as log is not done yet)
            return "ERR"

        # Extra cases:
        elif base == var and pow.strip() == '1': # For convering 'x ^ 1' to 'x'
            return Node(var, 'base')
        
        else: # In case of complex exponential or constant to constant
            print("COMPLEX CASE!!!") # Need log function for this
            

    elif root_val == '*':
        u = root_node.left_node
        v = root_node.right_node
        du = Differentiate(u, var = var)
        dv = Differentiate(v, var = var)

        new_node = Node('+', 'optr') # (du * v) + (dv * u)

        new_node.left_node = Node('*', 'optr')
        new_node.right_node = Node('*', 'optr')

        new_node.left_node.left_node = du
        new_node.left_node.right_node = v
        
        new_node.right_node.left_node = dv
        new_node.right_node.right_node = u

        return new_node

    elif root_val == '/':
        u = root_node.left_node
        v = root_node.right_node
        du = Differentiate(u, var = var)
        dv = Differentiate(v, var = var)

        # Root
        new_node = Node('/', 'optr') # ((du * v) - (dv * u)) / (v ^ 2)

        # - and ^:
        new_node.left_node = Node('-', 'optr')
        new_node.right_node = Node('^', 'optr')

        # Operands for - : * and *
        new_node.left_node.left_node = Node('*', 'optr')
        new_node.left_node.right_node = Node('*', 'optr')

        # Operands for ^:
        new_node.right_node.left_node = v
        new_node.right_node.right_node = Node('2', 'base')

        # Operands for each of the *:
        new_node.left_node.left_node.left_node = du
        new_node.left_node.left_node.right_node = v

        new_node.left_node.right_node.left_node = dv
        new_node.left_node.right_node.right_node = u

        return new_node


    elif root_val == '+' or root_val == '-':
        left_diff = Differentiate(root_node.left_node, var = var) # Left side
        right_diff = Differentiate(root_node.right_node, var = var) # Right side

        new_node = Node(root_val, 'optr')

        new_node.left_node = left_diff
        new_node.right_node = right_diff

        return new_node
        
    else: # For x and c:
        if root_val ==  var:
            root_val = derivatives.var() # Returns 1 always
        else: # Constant
            root_val = derivatives.const() # Always returns 0

        return Node(root_val, 'base')