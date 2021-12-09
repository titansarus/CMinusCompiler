import states
from lexer import Lexer
from lexer_output_generator import *
from lexer_file_writer import *
from cminus_parser import Parser
from parse_tree_generator import *

if __name__ == '__main__':
    states.initialize_states()
    lexer = Lexer()
    parser = Parser(lexer)
    initial_node = parser.parse()
    tree = get_tree(initial_node)
    with open("parse_tree.txt", "w") as f:
        print(render_tree(tree), file=f)