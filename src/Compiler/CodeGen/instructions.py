class Instruction:
    def __init__(self, operation):
        self.operation = operation
    def to_code(self):
        return f"({self.operation}, , , )"

class Add(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__("ADD")
        self.A1 = A1
        self.A2 = A2
        self.R = R
    def to_code(self):
        return f"({self.operation}, {A1}, {A2}, {R})"

class Mult(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__("MULT")
        self.A1 = A1
        self.A2 = A2
        self.R = R
    def to_code(self):
        return f"({self.operation}, {A1}, {A2}, {R})"

class Sub(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__("SUB")
        self.A1 = A1
        self.A2 = A2
        self.R = R
    def to_code(self):
        return f"({self.operation}, {A1}, {A2}, {R})"

class Eq(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__("EQ")
        self.A1 = A1
        self.A2 = A2
        self.R = R
    def to_code(self):
        return f"({self.operation}, {A1}, {A2}, {R})"

class LT(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__("LT")
        self.A1 = A1
        self.A2 = A2
        self.R = R
    def to_code(self):
        return f"({self.operation}, {A1}, {A2}, {R})"

class Assign(Instruction):
    def __init__(self, A, R):
        super().__init__("ASSIGN")
        self.A = A
        self.R = R
    def to_code(self):
        return f"({self.operation}, {A}, {R}, )"

class JPF(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__("JPF")
        self.A = A
        self.L = L
    def to_code(self):
        return f"({self.operation}, {A}, {L}, )"

class JP(Instruction):
    def __init__(self, L):
        super().__init__("JP")
        self.L = L
    def to_code(self):
        return f"({self.operation}, {L}, , )"

class Print(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__("PRINT")
        self.A = A
    def to_code(self):
        return f"({self.operation}, {A}, , )"