from Compiler.CodeGen.three_address_generator import *
from Compiler.Lexer import lexer_states
from Compiler.Lexer.lexer import Lexer
from Compiler.Parser.cminus_parser import Parser
from Compiler.CodeGen.codegen import CodeGen
from Compiler.Constants.constants import DEBUG

# Written by Soroush Jahanzad (98100389) and Amirmahdi Namjoo (97107212)
# Department of Computer Engineering - Sharif University of Technology

if __name__ == '__main__':
    lexer_states.initialize_states()
    lexer = Lexer("input.txt")
    codegen = CodeGen()
    parser = Parser(lexer, codegen)
    initial_node, errors, program, semantic_errors = parser.parse()
    if len(semantic_errors) == 0:
        result_program = generate_code(program)
        semantic_errors = ["The input program is semantically correct."]
    else:
        result_program = "The output code has not been generated."
    with open("output.txt", "w", encoding="utf-8") as f:
        print(result_program, file=f)
    with open("semantic_errors.txt", "w", encoding="utf-8") as f:
        print("\n".join(semantic_errors), file=f)

    if DEBUG:
        with open("debug.txt", "w", encoding="utf-8") as f:
            for line in codegen.line_map:
                ptoken = line[1][0]
                ntoken = line[1][1]
                if ptoken:
                    f.write(f"{line[0]} -> {ptoken.lexeme}, {ptoken.lineno}\n")
