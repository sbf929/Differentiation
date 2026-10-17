"Functions, operations, variables and other such stuff."
from ..data_struct import Node
from  ..parsing import CreateTree, CollapseTree, remove_wrapped_brackets
import copy
from ..CONFIG import ref as REFERENCE


class Function:
    """
    Class for function `name`(`parameters`).
    **`fn` should be a function of `parameters`.**
    - `name`: Name of the function
    - `parameters`: List of the variables that the initial function is made of
    - `fn`: Parametrized function expression 
    [Need domain for each vairables]
    """
    
    def __init__(self, name: str = 'f', parameters: tuple = ('x',), fn: str = 'x', 
                 domains: tuple = (('-inf', 'inf'))):
        self.name = name
        self.params: tuple = parameters
        self.fn_tree: Node = None
        self.domains = domains
        
        # Initialize function tree:
        self.initialize_fn_tree(fn)
  

    # Class behavior
    def __str__(self):
        param_string = ""
        for param in self.params:
            param_string += param
            param_string += ','

        return (f"{self.name}({param_string}) = {remove_wrapped_brackets(CollapseTree(self.fn_tree))} : {self.domains}")

    def __call__(self, args:tuple):
        "`args` can be string literals expressing variables or function or `Node` as well (A function tree)."
        # TODO once i complete the parametrized function.
        if len(args) != len(self.params):
            print("INVALID NUMBER OF ARGUMENTS PASSED.")
            return None

        return self.parameterize_function(args)

    # Operations:
    def _combine(self, other, operator) -> Function:
        # Add the function bodies:
        new_node = Node(operator, dtype=REFERENCE['dtype']['optr'])
        new_node.left_node = copy.deepcopy(self.fn_tree)
        new_node.right_node = copy.deepcopy(other.fn_tree)

        # Domain: TODO LATER

        # Parameters:
        new_params = tuple(dict.fromkeys(
                    (*self.params, *other.params)
                ))
        
        return Function(name = f"{self.name} {operator} {other.name}", parameters = new_params,
                        fn=remove_wrapped_brackets(CollapseTree(new_node)), domains=self.domains) # The domain part is ofc not right rn

    
    def __add__(self, other: Function) -> Function:
        return self._combine(other, '+')

    def __sub__(self, other):
        return self._combine(other, '-')

    def __mul__(self, other):
        return self._combine(other, '*')

    def __truediv__(self, other):
        return self._combine(other, '/')

    def __pow__(self, other):
        return self._combine(other, '^')
        

    # Structural functions:
    def initialize_fn_tree(self, fn) -> Node:
        #print("Initializing:\n", CreateTree(fn))
        self.fn_tree = CreateTree(fn)

    def parameterize_function(self, args:list):
        "Replaces node value. Needed to put the variable(s) in place of the parameters in the function."
        fn_tree_dup = copy.deepcopy(self.fn_tree)

        # Build argument-parameter dict:
        arg_param_zipped = dict(zip(self.params, args))
        print(arg_param_zipped)

        self._replace_variable_nodes(fn_tree=fn_tree_dup, arg_param_dict=arg_param_zipped)

        # Build parameter list:
        new_params = []

        for arg in args:
            if isinstance(arg, Function):
                new_params.extend(arg.params)
            else:
                new_params.append(arg)

        new_params = tuple(dict.fromkeys(new_params))

        return Function(name=self.name, parameters=new_params, fn=remove_wrapped_brackets(CollapseTree(fn_tree_dup)), domains=self.domains)

    def _replace_variable_nodes(self, fn_tree: Node, arg_param_dict: dict): # PRIVATE
        "`arg_param_dict`: Reference dict for replacing arguments with parameters. eg: {'x': '3', 'y': 'a'}"
        # TOP DOWN APPROACH:
        if fn_tree.left_node: 
            if fn_tree.left_node.left_node is None and fn_tree.left_node.right_node is None: # If this is a leaf
                # Check if its a parameter and substitute:
                if fn_tree.left_node.value in arg_param_dict:
                    # Check if argument is a Function:
                    if isinstance(arg_param_dict[fn_tree.left_node.value], Function):
                        print("GIVEN FUNCTION.")
                        new_left_node = copy.deepcopy(arg_param_dict[fn_tree.left_node.value].fn_tree)
                    else: # Create new substitution node if not Function:
                        new_left_node = CreateTree(arg_param_dict[fn_tree.left_node.value])

                    fn_tree.left_node = new_left_node

            else: # if its not a leaf check children (Recursion)
                self._replace_variable_nodes(fn_tree.left_node, arg_param_dict)

        if fn_tree.right_node: 
            if fn_tree.right_node.left_node is None and fn_tree.right_node.right_node is None:
                if fn_tree.right_node.value in arg_param_dict:
                    if isinstance(arg_param_dict[fn_tree.right_node.value], Function):
                        new_right_node = copy.deepcopy(arg_param_dict[fn_tree.right_node.value].fn_tree)
                    else:
                        new_right_node = CreateTree(arg_param_dict[fn_tree.right_node.value])

                    fn_tree.right_node = new_right_node

            else:
                self._replace_variable_nodes(fn_tree.right_node, arg_param_dict)


    # Function Operations:
    def compose_domains(self):
        'For set operations on domain to find the new domain of composite functions and all.'
        # INTERSECT domain:


    # Calculus: TODO LATER
    def differentiate(order: int = 1, mode: str = 'exp') -> str | Node:
        pass

    def integrate(mode: str = 'exp') -> str | Node:
        pass

