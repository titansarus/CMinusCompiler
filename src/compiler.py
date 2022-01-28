from Compiler.Parser.parse_tree_generator import *
from Compiler.Lexer import lexer_states
from Compiler.Lexer.lexer import Lexer
from Compiler.Parser.cminus_parser import Parser
from Compiler.CodeGen.codegen import CodeGen

if __name__ == '__main__':
    lexer_states.initialize_states()
    lexer = Lexer("input.txt")
    codegen = CodeGen()
    parser = Parser(lexer, codegen)
    initial_node, errors = parser.parse()
    if len(errors) == 0:
        errors = ["There is no syntax error."]
    tree = get_tree(initial_node)
    with open("parse_tree.txt", "w", encoding="utf-8") as f:
        print(render_tree(tree), file=f)
    with open("syntax_errors.txt", "w", encoding="utf-8") as f:
        print("\n".join(errors), file=f)
