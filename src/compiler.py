from Compiler.CodeGen.three_address_generator import *
from Compiler.Lexer import lexer_states
from Compiler.Lexer.lexer import Lexer
from Compiler.Parser.cminus_parser import Parser
from Compiler.CodeGen.codegen import CodeGen

if __name__ == '__main__':
    lexer_states.initialize_states()
    lexer = Lexer("input.txt")
    codegen = CodeGen()
    parser = Parser(lexer, codegen)
    initial_node, errors, program = parser.parse()
    if len(errors) == 0:
        errors = ["There is no syntax error."]
    with open("output.txt", "w", encoding="utf-8") as f:
        print(generate_code(program), file=f)
    with open("syntax_errors.txt", "w", encoding="utf-8") as f:
        print("\n".join(errors), file=f)
