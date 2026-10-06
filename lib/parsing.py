from .data_struct import Tree, Node
from .CONFIG import ref as REFERENCE


def remove_wrapped_brackets(exp: str) -> str:
    """Removes ALL wrapping brackets if they enclose the entire expression."""
    while True:
        if len(exp) < 2:
            return exp

        if exp[0] != '(' or exp[-1] != ')': # NO changes to be made if the first and last character arent brackets
            return exp

        # Real stuff now:
        bracket_count = 0
        wrapped = True

        for i, c in enumerate(exp):

            if c == '(':
                bracket_count += 1

            elif c == ')':
                bracket_count -= 1

            # Outer bracket closes before expression ends
            if bracket_count == 0 and i != len(exp) - 1:
                wrapped = False
                break

        if not wrapped:
            return exp

        # Remove ONE outer layer and repeat
        exp = exp[1:-1]

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
            precedence = REFERENCE['operator'][c]['precedence']
            associativity = REFERENCE['operator'][c]['associativity']

            if precedence < temp_precedence:
                root_idx = i
                temp_precedence = precedence

            elif precedence == temp_precedence and associativity == 'left':
                root_idx = i
                    

    return root_idx


def resolve_function(exp: str) -> Node | None:
    """Resolves function: f(u(x)) to f(x) --> u(x). (Only limited to 1 term so it does not parse u(x))\nFor a non function return `None`."""
    new_node = None
    bracket_depth = 0
    bracket_found = False
    start_i = None
    end_i = None

    # Identifying f(u(x)):
    fn_sorted_lst = sorted(REFERENCE['function'].keys(), key=len, reverse=True)  # Sorted list had to be added as 'cosec' and 'cos' mixed up

    for fn in fn_sorted_lst:
        if exp.startswith(fn): # f is found
            # Find u(x):
            for i, c in enumerate(exp):
                if c == '(':
                    bracket_depth += 1

                    if not bracket_found: # u starts from here
                        start_i = i
                        bracket_found = True

                if c == ')':
                    bracket_depth -= 1

                if bracket_found and bracket_depth == 0:
                    end_i = i  
                    break

            u = remove_wrapped_brackets(exp[start_i + 1:end_i])
            f = exp[:start_i]

            # Create Node:
            new_node = Node(f, REFERENCE['dtype']['fn'])

            if fn == 'log_': # Special case for log (2 parameters)
                # TODO THIS NEEDS TO BE WORKED LATER ON AS IT CANNOT HANDLE BASES such as 40, 100 etc
                base = exp[4]
                new_node.value = new_node.value[:4]
                new_node.left_node = Node(base, REFERENCE['dtype']['leaf'])

            new_node.right_node = Node(u, REFERENCE['dtype']['complex'])

            break

    return new_node

def parse(exp: str) -> Node:
    """
    Generates a Child <- Node -> Child for given `exp` based on the root operator in it. Returns `Node`. For parsing one single term.
    """
    # Dealing with barckets and whitespaces:
    exp = exp.strip()
    exp = remove_wrapped_brackets(exp)

    # Initialize tree with master nodes and its children:
    root_optr_idx = find_root_operation(exp)

    if root_optr_idx is None: # No operator found in exp (Can be a function or a leaf)
        # Check if function:
        new_node = resolve_function(exp)
        if new_node is not None:
            return new_node # returns 'fn' type node
        
        else: # exp is not a function thus it is a leaf
            return Node(exp, REFERENCE['dtype']['leaf']) # Returns 'leaf' type node


    # If root operator is found make it the root node:
    root_optr = exp[root_optr_idx] 
    new_node = Node(root_optr, REFERENCE['dtype']['optr']) 

    # Attach rest of the expression to root node:
    new_node.left_node = Node(exp[:root_optr_idx], REFERENCE['dtype']['complex'])
    new_node.right_node = Node(exp[root_optr_idx + 1:], REFERENCE['dtype']['complex'])

    return new_node # Return 'optr' type node


def CreateTree(exp: str) -> Node:
    "Returns the fully parsed `exp` as `Node`. **Recursive**"
    new_node = parse(exp)

    if new_node.dtype == REFERENCE['dtype']['leaf']:
        return new_node # If the node is a leaf 

    # Parse left subtree:
    if new_node.left_node:
        new_node.left_node = CreateTree(new_node.left_node.value)

    # Parse right subtree:
    if new_node.right_node:
        new_node.right_node = CreateTree(new_node.right_node.value)

    return new_node





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
    # Leaf: (No children)
    if node.left_node is None and node.right_node is None:
        return node.value

    # Function:
    if node.value == 'log_': # SPECIAL EDGE CASE FOR log
            right = CollapseTree(node.right_node)
            base = node.left_node.value
            return f"{node.value}{base}({right})"
    
    if node.left_node is  None and node.right_node is not None:
        right = CollapseTree(node.right_node)
        return f"{node.value}({right})"
        

    # Building one single term:
    if node.left_node is not None:
        left = CollapseTree(node.left_node) # Left side of expression
    if node.right_node is not None:
        right = CollapseTree(node.right_node) # Right side of expression

    return f"({left} {node.value} {right})"
        