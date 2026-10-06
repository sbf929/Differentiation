class Stack:
    def __init__(self, max_len = None):
        self.stack = []
        self.max_len = max_len

    # Getters:
    def _get_stack(self):
        return self.stack

    # Class functions:

    def push(self, val):
        "Push `val` into the stack."
        if self.max_len != None:
            # Check current length:
            if len(self.stack) == self.max_len:
                print(f"STACK IS FULL")
                return 

        self.stack.append(val)

    def pop(self):
        "Pops and returns the top most element in the stack."
        if len(self.stack) == 0:
            print("Stack empty.")
            return
        
        item = self.stack.pop()
        return item

    def peek(self):
        pass

    def display(self):
        "Displays the full stack."
        print(self.stack)


class Node:
    "Stores a value `val` of data type `dtype`. Both parameters need to be intialized."
    def __init__(self, val:str, dtype:str):
        self.value = val
        self.dtype = dtype # oprd / optr

        self.parent_node: Node = None 

        self.left_node: Node = None
        self.right_node: Node = None

    # No idea how __str__ and _str_node works (CHAT GPT):
    def __str__(self):
        return self._str_node()

    def _str_node(self, indentation=0):
        if self is None:
            return ""

        result = ""

        # Right subtree
        if self.right_node is not None:
            result += self.right_node._str_node(indentation + 1)

        # Current node
        result += "    " * indentation
        result += f"{self.value}\n"

        # Left subtree
        if self.left_node is not None:
            result += self.left_node._str_node(indentation + 1)

        return result

    def __eq__(self, other):
        return (
            self.__str__() == other.__str__()
        )
        
class Tree:
    """
    ### Binary Tree structure.\n
    For Compiling a mathematical expression.\n 
    Parent node should represents **Operator**.
    Child Nodes:
    - Left node should represent the **preceding operand**.
    - Right node should represent the **suceeding operand**.
    """
    def __init__(self, master_node: Node):
        self.master_node = master_node

    # No idea how __str__ and _str_node works (CHAT GPT):
    def __str__(self):
        return self._str_node(self.master_node)

    def _str_node(self, node, indentation=0):
        if node is None:
            return ""

        result = ""

        result += self._str_node(node.right_node, indentation + 1)

        result += "    " * indentation
        result += f"{node.value}\n"

        result += self._str_node(node.left_node, indentation + 1)

        return result
        
    # Node functions:
    def create_node(self, val, dtype):
        return Node(val, dtype)

    def link_nodes(self, parent:Node, child:Node, direction:int):
        if direction == -1:
            parent.left_node = child
            child.parent = parent

        elif direction == 1:
            parent.right_node = child
            child.parent = parent

        else:
            raise ValueError("Direction must be -1 or 1")