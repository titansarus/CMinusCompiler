DEBUG = True

letters = "qwertyuiopasdfghjklmnbvcxzQWERTYUIOPLKJHGFDSAZXCVBNM"
digits = "0123456789"
symbol = ";:,[](){}+-*=<"
whitespace = "\n\r\t\v\f "
slash = "/"
all_valid = letters + digits + symbol + whitespace + slash
keywords = ["if", "else", "void", "int", "repeat", "break", "until", "return", "endif"]
NUM = "NUM"
ID = "ID"
KEYWORD = "KEYWORD"
KEYWORD_ID = "KEYWORD_ID"
SYMBOL = "SYMBOL"
COMMENT = "COMMENT"
WHITESPACE = "WHITESPACE"
START = "START"
FINISH = "FINISH"
END_TOKEN = "END_TOKEN"
EPSILON = "epsilon"
TOKEN_TYPES = [NUM, ID, KEYWORD, KEYWORD_ID, SYMBOL, COMMENT, WHITESPACE, START, END_TOKEN]
all_characters = "".join([chr(i) for i in range(256)])

INT = "int"
VOID = "void"
ARRAY = "array"

PANIC_INVALID_INPUT = "Invalid input"
PANIC_INVALID_NUMBER = "Invalid number"
PANIC_UNMATCHED_COMMENT = "Unmatched comment"
PANIC_UNCLOSED_COMMENT = "Unclosed comment"

PANIC_STATES = [PANIC_INVALID_INPUT, PANIC_INVALID_NUMBER, PANIC_UNMATCHED_COMMENT, PANIC_UNCLOSED_COMMENT]

NUM_ID_PARSER_EDGE = "NUM_ID_PARSER_EDGE"
KEYWORD_SYMBOL_PARSER_EDGE = "KEYWORD_SYMBOL_PARSER_EDGE"
PRODUCTION_PARSER_EDGE = "PRODUCTION_PARSER_EDGE"
EPSILON_PARSER_EDGE = "EPSILON_PARSER_EDGE"
ACTION_PARSER_EDGE = "ACTION_PARSER_EDGE"
PARSER_EDGE_TYPES = [NUM_ID_PARSER_EDGE, KEYWORD_SYMBOL_PARSER_EDGE, PRODUCTION_PARSER_EDGE, EPSILON_PARSER_EDGE,
                     ACTION_PARSER_EDGE]

DIAGRAM_ENDED = "DIAGRAM_ENDED"
NO_WAY_IN_DIAGRAM = "NO_WAY_IN_DIAGRAM"

WORD_SIZE = 4
CODE_SECTION_START_ADDRESS = 0
DATA_SECTION_START_ADDRESS = 100000
TEMP_SECTION_START_ADDRESS = 500004
STACK_START_ADDRESS = TEMP_SECTION_START_ADDRESS - WORD_SIZE
STACK_PUSH_INSTRUCTION_COUNT = 2

SCOPE_SEMANTIC_ERROR = "Semantic Error! '{}' is not defined."
VOID_SEMANTIC_ERROR = "Semantic Error! Illegal type of void for '{}'."
ARG_COUNT_MISMATCH_SEMANTIC_ERROR = "Semantic Error! Mismatch in numbers of arguments of '{}'."
BREAK_SEMANTIC_ERROR = "Semantic Error! No 'repeat ... until' found for 'break'."
OPERAND_TYPE_MISMATCH_SEMANTIC_ERROR = "Semantic Error! Type mismatch in operands, Got {} instead of {}."
ARG_TYPE_MISMATCH_SEMANTIC_ERROR = "Semantic Error! Mismatch in type of argument {} of '{}'. Expected '{}' but got '{}' instead."
