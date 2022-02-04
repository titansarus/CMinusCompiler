class Instruction:
    def __init__(self, operation):
        self.operation = operation

    def to_code(self):
        return f"({self.operation}, , , )"


class Add(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__('ADD')
        self.A1 = A1
        self.A2 = A2
        self.R = R

    def to_code(self):
        return f"({self.operation}, {self.A1}, {self.A2}, {self.R})"


class Mult(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__('MULT')
        self.A1 = A1
        self.A2 = A2
        self.R = R

    def to_code(self):
        return f"({self.operation}, {self.A1}, {self.A2}, {self.R})"


class Sub(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__('SUB')
        self.A1 = A1
        self.A2 = A2
        self.R = R

    def to_code(self):
        return f"({self.operation}, {self.A1}, {self.A2}, {self.R})"


class Eq(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__('EQ')
        self.A1 = A1
        self.A2 = A2
        self.R = R

    def to_code(self):
        return f"({self.operation}, {self.A1}, {self.A2}, {self.R})"


class LT(Instruction):
    def __init__(self, A1, A2, R):
        super().__init__('LT')
        self.A1 = A1
        self.A2 = A2
        self.R = R

    def to_code(self):
        return f"({self.operation}, {self.A1}, {self.A2}, {self.R})"


class Assign(Instruction):
    def __init__(self, A, R):
        super().__init__('ASSIGN')
        self.A = A
        self.R = R

    def to_code(self):
        return f"({self.operation}, {self.A}, {self.R}, )"


class JPF(Instruction):
    def __init__(self, A, L):
        super().__init__('JPF')
        self.A = A
        self.L = str(L)

    def to_code(self):
        L = self.L
        if L[0] == '#':
            L = L[1:]
        else:
            L = '@' + L
        return f"({self.operation}, {self.A}, {L}, )"


class JP(Instruction):
    def __init__(self, L):
        super().__init__('JP')
        self.L = str(L)

    def to_code(self):
        L = self.L
        if L[0] == '#':
            L = L[1:]
        else:
            L = '@' + L
        return f"({self.operation}, {L}, , )"


class Print(Instruction):
    def __init__(self, A):
        super().__init__('PRINT')
        self.A = A

    def to_code(self):
        return f"({self.operation}, {self.A}, , )"
