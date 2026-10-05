from .data_struct import Tree, Node
from .CONFIG import ref as REFERENCE


def wrapped_bracket_remover(exp: str) -> str:
    """Removes wrapping brackets if they enclose the entire expression."""

    if exp[0] != '(' or exp[-1] != ')': # NO changes to be made if the first and last character arent brackets
        return exp

    bracket_count = 0

    for i, c in enumerate(exp):
        if c == '(':
            bracket_count += 1

        elif c == ')':
            bracket_count -= 1

        # Outer bracket closed before the expression ended.
        if bracket_count == 0 and i != len(exp) - 1: # Needed for cases such as exp = '(x + 5) + (x - 6)'
            return exp

    return exp[1:-1] # Returns str with the 2(start and end) brackets removed

# The bracket checking is issue in case of expression wrapped inside racket returs None instead of index
def find_root_operation(exp:str) -> int:
    "Returns the index of the **root operator** in `exp`."
    root_idx = None # OUTPUT

    temp_precedence = 999
    bracket_count = 0 # Bracket depth within the expression

    # Go through each character:
    for i, c in enumerate(exp):
        if c == '(': # Going inside a bracket
            bracket_count += 1

        if c == ')': # Coming out of a brakcet
            bracket_count -= 1

        # Check if operator and only if not in a bracket heirarchy
        if bracket_count == 0 and c in REFERENCE['operator'].keys():
            # Check if precedence is lower than the curent selected:
            if REFERENCE['operator'][c]['precedence'] < temp_precedence:
                root_idx = i
                temp_precedence = REFERENCE['operator'][c]['precedence'] # Update lowest predecence temp

    return root_idx


def resolve_function(exp: str) -> Node:
    """Resolves function: f(u(x)) to f(x) --> u(x). (Only limited to 1 term so it does not parse u(x))"""

def parse(exp: str) -> Node:
    """
    Generates a Child <- Node -> Child for given `exp` based on the root operator in it. Returns `Node`. For parsing one single term.
    """
    # Dealing with barckets:
    exp = exp.strip()
    exp = wrapped_bracket_remover(exp)

    # Initialize tree with master nodes and its children:
    root_optr_idx = find_root_operation(exp)

    if root_optr_idx is None: # No operator found in exp
        return Node(exp, 'base') # Change its type to `base`


    root_optr = exp[root_optr_idx] # get the root operator from the exp string

    new_node = Node(root_optr, 'optr') # return this Node

    # Attach the rest of the expression as children Nodes:
    # partition = exp.partition(root_optr) NOT TO BE USED AS IT TAKES THE FIRST INSTANCE OF THE OPERATOR INSTEAD OF THE SPECIFIED INDEX
    # USE INDEXING INSTEAD

    new_node.left_node = Node(exp[:root_optr_idx], 'complex')
    new_node.right_node = Node(exp[root_optr_idx + 1:], 'complex')

    return new_node



def CreateTree(exp: str) -> Node:
    "Returns the fully parsed `exp` as `Node`. **Recursive**"
    #print("Parsing:", exp)

    node = parse(exp)

    #print("Result:", node.value, node.dtype)

    # For base:
    if node.dtype == 'base':
        return node

    # Parse left subtree:
    node.left_node = CreateTree(node.left_node.value)

    # Parse right subtree:
    node.right_node = CreateTree(node.right_node.value)

    return node








# THIS THING IS NOT WORKING: WILL LATER MOVE IN /math module 
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

# Final thing:
def CollapseTree(node: Node) -> str:
    "Collapses a given `Node` into a expression: `str`."
    # Check if this node is a leaf: (No children)
    if node.left_node is None and node.right_node is None:
        return node.value

    # Building one single term:
    if node.left_node is not None:
        left = CollapseTree(node.left_node) # Left side of expression
    if node.right_node is not None:
        right = CollapseTree(node.right_node) # Right side of expression

    return f"({left} {node.value} {right})"
        