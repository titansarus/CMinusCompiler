class Token:
    def __init__(self, lineno=None, token_type=None, lexeme=None, must_continue=False):
        self.lineno = lineno
        self.token_type = token_type
        self.lexeme = lexeme
        self.must_continue = must_continue

    def __str__(self):
        return f"({self.lineno}, '{self.token_type}', '{self.lexeme}', {self.must_continue})".encode(
            "unicode_escape").decode("utf-8")
