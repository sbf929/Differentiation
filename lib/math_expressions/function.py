"Functions, operations, variables and other such stuff."
from ..data_struct import Node
from  ..parsing import CreateTree, CollapseTree, remove_wrapped_brackets
import copy


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
        return (f"{self.name}({", ".join(self.params)}) : {self.domains}")

    def __call__(self, args:list):
        # TODO once i complete the parametrized function.
        if len(args) != len(self.params):
            print("INVALID NUMBER OF ARGUMENTS PASSED.")
            return None

        return self.parameterize_function(args)

    def __add__(self, other) -> Function:
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __pow__(self, other):
        pass

    # Structural functions:
    def initialize_fn_tree(self, fn) -> Node:
        #print("Initializing:\n", CreateTree(fn))
        self.fn_tree = CreateTree(fn)

    def build_fn_tree(self, arg_var: list) -> Node:
        if len(arg_var) != len(self.params):
            print('ERR: Function argument number not matching')

        pass

    def parameterize_function(self, args:list):
        "Replaces node value. Needed to put the variable(s) in place of the parameters in the function."
        fn_tree_dup = copy.deepcopy(self.fn_tree)

        # Build argument-parameter dict:
        arg_param_zipped = dict(zip(self.params, args))
        print(arg_param_zipped)

        self._replace_variable_nodes(fn_tree=fn_tree_dup, arg_param_dict=arg_param_zipped)

        return fn_tree_dup

    def _replace_variable_nodes(self, fn_tree: Node, arg_param_dict: dict): # PRIVATE
        "`arg_param_dict`: Reference dict for replacing arguments with parameters. eg: {'x': '3', 'y': 'a'}"
        # TOP DOWN APPROACH:
        if fn_tree.value in arg_param_dict: # Replace it with param:
            fn_tree.value = arg_param_dict[fn_tree.value]

        # Recurse into children nodes:
        if fn_tree.left_node: 
            self._replace_variable_nodes(fn_tree.left_node, arg_param_dict)
        if fn_tree.right_node: 
            self._replace_variable_nodes(fn_tree.right_node, arg_param_dict)

        

    # Calculus: TODO LATER
    def differentiate(order: int = 1, mode: str = 'exp') -> str | Node:
        pass

    def integrate(mode: str = 'exp') -> str | Node:
        pass




class var:
    pass