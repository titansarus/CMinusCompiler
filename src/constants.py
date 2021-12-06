
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
TOKEN_TYPES = [NUM, ID, KEYWORD, KEYWORD_ID, SYMBOL, COMMENT, WHITESPACE, START, END_TOKEN]
all_characters = "".join([chr(i) for i in range(256)])

PANIC_INVALID_INPUT = "Invalid input"
PANIC_INVALID_NUMBER = "Invalid number"
PANIC_UNMATCHED_COMMENT = "Unmatched comment"
PANIC_UNCLOSED_COMMENT = "Unclosed comment"

PANIC_STATES = [PANIC_INVALID_INPUT, PANIC_INVALID_NUMBER, PANIC_UNMATCHED_COMMENT, PANIC_UNCLOSED_COMMENT]
