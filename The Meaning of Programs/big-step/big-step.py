class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def evaluate(self, environment):
        return self


class Boolean:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def __eq__(self, other):
        if not isinstance(other, Boolean):
            return False
        return self.value == other.value

    def evaluate(self, environment):
        return self


class Varible:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"

    def evaluate(self, environment):
        return environment.get(self.name)


class DoNothing:
    def __repr__(self):
        return 'do-nothing'

    def __eq__(self, other):
        return isinstance(other, DoNothing)

    def evaluate(self, environment):
        return environment


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} + {self.right}"

    def evaluate(self, environment):
        return Number(self.left.evaluate(environment).value
                      + self.right.evaluate(environment).value)


class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} * {self.right}"

    def evaluate(self, environment):
        return Number(self.left.evaluate(environment).value
                      * self.right.evaluate(environment).value)


class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} < {self.right}"

    def evaluate(self, environment):
        return Boolean(self.left.evaluate(environment).value
                       < self.right.evaluate(environment).value)


class Assign:
    reducible = True

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f"{self.name} = {self.expression}"

    def evaluate(self, environment):
        environment.update({self.name: self.expression.evaluate(environment)})
        return environment


class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __repr__(self):
        return f"if ({self.condition}) {{{self.consequence}}} else {{{self.alternative}}}"

    def evaluate(self, environment):
        cond = self.condition.evaluate(environment)
        if cond == Boolean(True):
            return self.consequence.evaluate(environment)
        else:
            return self.alternative.evaluate(environment)


class Sequence:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return f"{self.first}, {self.second}"

    def evaluate(self, environment):
        return self.second.evaluate(self.first.evaluate(environment))


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"while ({self.condition}) {{{self.body}}}"

    def evaluate(self, environment):
        if self.condition.evaluate(environment) == Boolean(True):
            return self.evaluate(self.body.evaluate(environment))
        else:
            return environment


if __name__ == '__main__':
    print(Number(23).evaluate({}))
    print(Varible('x').evaluate({'x': Number(23)}))

    exp = LessThan(Add(Varible('x'), Number(2)),
                   Varible('y'))
    exp_env = {'x': Number(2), 'y': Number(5)}
    res = exp.evaluate(exp_env)
    print(res)

    # sequence
    seq_exp = Sequence(Assign('x', Add(Number(1), Number(1))),
                       Assign('y', Add(Varible('x'), Number(3))))
    seq_res = seq_exp.evaluate({})
    print(seq_res)

    # while
    while_exp = While(LessThan(Varible('x'), Number(5)),
                      Assign('x', Multiply(Varible('x'), Number(3))))
    while_env = {'x': Number(1)}
    while_res = while_exp.evaluate(while_env)
    print(while_res)



