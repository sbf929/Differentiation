from ..data_struct import Node
from ..CONFIG import ref as REFERENCE

# Commutative: a + b = b + a and ab = ba
def commutative_transform(node: Node) -> Node:
    "Converts [a] <- [root node] -> [b] into [b] <- [root node] -> [a]"
    if node.value == '+' or node.value == '*' and node.left_node and node.right_node:
        new_node = Node(node.value, node.dtype)
        new_node.left_node = node.right_node
        new_node.right_node = node.left_node

        return new_node

    return node


# Associative: (a + b) + c = a + (b + c): I DONT THINK ANYTHING NEEDS TO BE DONE HERE


# Distributive: a(b +&- c) = a*b +&- a*c and speial case of -(a + b) = -a - b
def distributive_transform(node: Node) -> Node:
    "Distrubutes outside factor among inside terms given root node is **\*** with either the left or the right node having **+** or **-**"
    if node.value == '*':
        # If both are having + or - eg: (x + 5)(x - 6) take the left term as the out_factor
        if node.left_node.value in ['+', '-']: # Right node is the out_factor
            out_factor = node.right_node
            in_term = node.left_node
        elif node.right_node.value in ['+', '-']: # Left node is the in_factor
            out_factor = node.left_node
            in_term = node.right_node # root node for this is + or -
        else:
            print("Cant applu distributive law.")
            return node

        # Building new node:
        new_node = Node('+', REFERENCE['dtype']['optr'])

        new_node.left_node = Node('*', REFERENCE['dtype']['optr'])
        new_node.right_node = Node('*', REFERENCE['dtype']['optr'])

        new_node.left_node.left_node = out_factor
        new_node.left_node.right_node = in_term.left_node

        new_node.right_node.left_node = out_factor
        new_node.right_node.right_node = in_term.right_node

        return new_node

    return node


# Sign: +(a) = a | -(a) = -a | -(-a) = + a or a
def identify_sign(term:str) -> str:
    "Returns the sign for a given term."
    if term.strip()[0] == '-':
        return '-'
    else:
        return '+'

def sign_transform(sign_1:str, sign_2:str) -> str:
    "Sign transformations"
    if sign_1 == sign_2:
        return '+'
    
    else:
        return '-'


# Addtive and multiplicative Laws: | a * 1 = a | a + 0 = a
def multiply_1(node: Node) -> Node:
    if node.value == '*':
        if node.left_node.value == '1':
            return node.right_node
        if node.right_node.value == '1':
            return node.left_node

    return node

def add_0(node: Node) -> Node:
    if node.value == '+':
        if node.left_node.value == '0':
            return node.right_node
        if node.right_node.value == '0':
            return node.left_node

    return node

# Additive inverse: a + (-a) or (-a) + a = 0


# Multiplicative inverse: a * (1 / a) = 1 [: If a not = 0]


# Zero multiplication and division: a * 0 = 0 | 0 / a = 0 | BUT | a / 0 = ERR
def multiply_0(node: Node) -> Node:
    if node.value == '*':
        if node.left_node.value == '0' or node.right_node.value == '0':
            return Node('0', REFERENCE['dtype']['leaf'])

    return node
        

# Fraction / Product relationships: (a/b) * (c/b) = (ac)/(bd) | (arg / (a/b)) = (arg * b) / a | a * (x/y) = (a*x) /y


# Exponential laws: 
# a ^ 1 = a | a ^ 0 = 1 | 1 ^ a = 1
# a^m * a ^ n | a ^ m / a ^ n 
def pow_of_1(node: Node) -> Node:
    if node.value == '^':
        if node.left_node.value == '1':
            return node.right_node
        if node.right_node.value == '1':
            return node.left_node

def pow_of_0(node: Node) -> Node:
    if node.value == '^':
        if node.left_node.value == '0' or node.right_node.value == '0':
            return Node('1', REFERENCE['dtype']['leaf'])

def power_sum(node: Node) -> Node:
    "a^m * a^n = a ^ (m + n)"
    if node.value == '*' and node.left_node.value == '^' and node.right_node.value == '^':
        # Check if bases are same:
        base_1 = node.left_node.left_node
        base_2 = node.right_node.left_node
        pow_1 = node.left_node.right_node
        pow_2 = node.right_node.right_node

        if base_1 == base_2:
            new_node = Node('^', REFERENCE['dtype']['optr'])
            new_node.left_node = base_1
            new_node.right_node = Node('+', REFERENCE['dtype']['optr'])

            new_node.right_node.left_node =  pow_1
            new_node.right_node.right_node = pow_2

            return new_node

    return node
