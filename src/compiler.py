import states
from lexer import Lexer
from lexer_output_generator import *
from lexer_file_writer import *
from cminus_parser import Parser

if __name__ == '__main__':
    states.initialize_states()
    lexer = Lexer()
    parser = Parser(lexer)
    initial_state = parser.parse()
    print(initial_state)