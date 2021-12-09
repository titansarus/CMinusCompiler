import states
from lexer import Lexer
from cminus_parser import Parser
from parse_tree_generator import *

if __name__ == '__main__':
    states.initialize_states()
    lexer = Lexer()
    parser = Parser(lexer)
    initial_node, errors = parser.parse()
    if len(errors) == 0:
        errors = ["There is no syntax error."]
    tree = get_tree(initial_node)
    with open("parse_tree.txt", "w") as f:
        print(render_tree(tree), file=f)
    with open("syntax_errors.txt", "w") as f:
        print("\n".join(errors), file=f)