class Number:
    reducible = False

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"


class Add:
    reducible = True

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} + {self.right}"

    def reduce(self):
        if self.left.reducible:
            return Add(self.left.reduce(),
                       self.right)
        elif self.right.reducible:
            return Add(self.left,
                       self.right.reduce())
        else:
            return Number(self.left.value + self.right.value)


class Multiply:
    reducible = True

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} * {self.right}"

    def reduce(self):
        if self.left.reducible:
            return Multiply(self.left.reduce(),
                            self.right)
        elif self.right.reducible:
            return Multiply(self.left,
                            self.right.reduce())
        else:
            return Number(self.left.value * self.right.value)


class Boolean:
    reducible = False

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"


class LessThan:
    reducible = True

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reduce(self):
        if self.left.reducible:
            return LessThan(self.left.reduce(),
                            self.right)
        elif self.right.reducible:
            return LessThan(self.left,
                            self.right.reduce())
        return Boolean(self.left.value < self.right.value)


class Machine:
    def __init__(self, expression):
        self.expression = expression

    def run(self):
        while self.expression.reducible:
            self.expression = self.expression.reduce()
        return self.expression


if __name__ == '__main__':
    expression_test = Add(Multiply(Number(1), Number(2)),
                          Multiply(Number(3), Number(4)))
    res = Machine(expression_test).run()
    print(res)
