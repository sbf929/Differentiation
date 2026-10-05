from lib import differentiate as diff, parsing as parser

def main():
    print("Welcome to Differential Calculator 1.0.1.\nCopyright (C) 2026 TIU, Inc.\nq() to quit.\n")

    while True:
        
        exp = input("!#> ")

        try:
            exp_tree = parser.CreateTree(exp) # Expression Tree
            diff_tree = diff.Differentiate(exp_tree, 'x') # Differential
            clean_diff_tree = parser.clean(diff_tree) # Cleaned
            print("   ", parser.CollapseTree(clean_diff_tree), '\n', ('_' * 150), "\n") # Collapsed

        except Exception as e:
            print("Invalid expression.\nERR:\n", e)
            raise(e)

        if exp == 'q()':
            break

main()