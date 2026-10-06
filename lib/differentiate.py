from .data_struct import Node
from . import derivatives

from . import parsing

from .CONFIG import ref as REFERENCE

def Differentiate(root_node: Node, var: str) -> Node:
    """
    - `root_node`: The root node of a term.
    - `var`: Variable to whose respect differentiation is to be done.
    """
    diff_ptr = root_node # Differential Pointer

    root_val = root_node.value
    
    # Basic operations:
    if root_val == '^': #TODO 
        u = root_node.left_node # Base
        v = root_node.right_node # Power

        u_pow_v = root_node # (u ^ v)

        dv = Differentiate(v, var) # dv
        du = Differentiate(u, var)

        ln_u = Node('log_', REFERENCE['dtype']['fn']) # ln(u)
        ln_u.left_node = Node('e', REFERENCE['dtype']['leaf'])
        ln_u.right_node = u

        # Building: (u^v) * ((dv * ln(u)) + (v * (du/u)))
        new_node = parsing.CreateTree(f"""({parsing.CollapseTree(u_pow_v)}) * 
                                                    (({parsing.CollapseTree(dv)} * {parsing.CollapseTree(ln_u)}) + 
                                                    ({parsing.CollapseTree(v)} * ({parsing.CollapseTree(du)} / {parsing.CollapseTree(u)})))""")

        return new_node
           
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
        
    else: # Can be x / const / function:
        # Functions: Need to pass (u(x)) instead of var:
        fn_sorted_lst = sorted(REFERENCE['function'].keys(), key=len, reverse=True) # Sorted list had to be added as 'cosec' and 'cos' mixed up

        for fn in fn_sorted_lst:
            if root_val.startswith(fn): # if function
                if root_val == 'log_': # Special case for log_
                    u = root_node.right_node
                    base = root_node.left_node.value
                    print("BASE:", base)
                    diff_exp = derivatives.logarithm(var, arg = parsing.CollapseTree(u), base = base) # TODO LATER

                elif REFERENCE['function'][fn]['ftype'] == 'trig': # Trignometric functions
                    u = root_node.right_node # u(x)
                    diff_exp = derivatives.trignometric(fn, arg = parsing.CollapseTree(u)) # f'(u(x)): Need to collapse u(x) as var: str

                elif REFERENCE['function'][fn]['ftype'] == 'inv trig': # Inverse trignometric functions
                    u = root_node.right_node # u(x)
                    diff_exp = derivatives.inv_trignometric(fn, arg = parsing.CollapseTree(u))

                new_node  = Node('*', REFERENCE['dtype']['optr']) # f'(u(x)) * u'(x)
                new_node.left_node = Node(diff_exp, REFERENCE['dtype']['complex'])
                new_node.right_node = Differentiate(u, var)

                return new_node



        if root_val ==  var:
            root_val = derivatives.var() # Returns 1 always
        else: # Constant
            root_val = derivatives.const() # Always returns 0

        return Node(root_val, 'base')