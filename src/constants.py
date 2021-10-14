from hashlib import sha1
from random import random

letters = "qwertyuiopasdfghjklmnbvcxzQWERTYUIOPLKJHGFDSAZXCVBNM"
digits = "0123456789"
symbol = ";:,[](){}+-*=<"
whitespace = "\n\r\t\v\f "
slash = "/"
all_valid = letters + digits + symbol + whitespace + slash
keywords = ["if", "else", "void", "int", "repeat", "break", "until", "return"]
NUM = "NUM"
ID = "ID"
KEYWORD = "KEYWORD"
KEYWORD_ID = "KEYWORD_ID"
SYMBOL = "SYMBOL"
COMMENT = "COMMENT"
WHITESPACE = "WHITESPACE"
START = "START"
TOKEN_TYPES = [NUM, ID, KEYWORD, KEYWORD_ID, SYMBOL, COMMENT, WHITESPACE, START]
all_characters = "".join([chr(i) for i in range(256)])
