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

    def reduce(self, environment):
        if self.left.reducible:
            return Add(self.left.reduce(environment),
                       self.right)
        elif self.right.reducible:
            return Add(self.left,
                       self.right.reduce(environment))
        else:
            return Number(self.left.value + self.right.value)


class Multiply:
    reducible = True

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} * {self.right}"

    def reduce(self, environment):
        if self.left.reducible:
            return Multiply(self.left.reduce(environment),
                            self.right)
        elif self.right.reducible:
            return Multiply(self.left,
                            self.right.reduce(environment))
        else:
            return Number(self.left.value * self.right.value)


class Boolean:
    reducible = False

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def __eq__(self, other):
        if not isinstance(other, Boolean):
            return False
        return self.value == other.value


class LessThan:
    reducible = True

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} < {self.right}"

    def reduce(self, environment):
        if self.left.reducible:
            return LessThan(self.left.reduce(environment),
                            self.right)
        elif self.right.reducible:
            return LessThan(self.left,
                            self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)


class Varible:
    reducible = True

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"

    def reduce(self, environment):
        return environment.get(self.name)


class DoNothing:
    reducible = False

    def __eq__(self, other):
        return isinstance(other, DoNothing)

    def __repr__(self):
        return 'do-nothing'


class Assign:
    reducible = True

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f"{self.name} = {self.expression}"

    def reduce(self, environment):
        if self.expression.reducible:
            return Assign(self.name,
                          self.expression.reduce(environment))
        else:
            environment.update({self.name: self.expression})
            return DoNothing(), environment


class If:
    reducible = True

    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __repr__(self):
        return f"if ({self.condition}) {{{self.consequence}}} else {{{self.alternative}}}"

    def reduce(self, environment):
        if self.condition.reducible:
            return If(self.condition.reduce(environment),
                      self.consequence,
                      self.alternative)
        else:
            if self.condition == Boolean(True):
                return self.consequence
            else:
                return self.alternative


class Sequence:
    reducible = True

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return f"{self.first}, {self.second}"

    def reduce(self, environment):
        if self.first != DoNothing():
            try:
                reduce_first, environment = self.first.reduce(environment)
            except TypeError:
                reduce_first = self.first.reduce(environment)
            return Sequence(reduce_first, self.second), environment
        else:
            return self.second, environment


class While:
    reducible = True

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"while ({self.condition}) {{{self.body}}}"

    def reduce(self, environment):
        return If(self.condition, Sequence(self.body, self), DoNothing())


class Machine:
    def __init__(self, expression, environment):
        self.expression = expression
        self.environment = environment

    def run(self):
        while self.expression.reducible:
            try:
                self.expression, self.environment = self.expression.reduce(self.environment)
            except TypeError:
                self.expression = self.expression.reduce(self.environment)
        return self.expression, self.environment


if __name__ == '__main__':
    exp = Add(Varible('x'), Varible('y'))
    exp_env = {
        'x': Number(3),
        'y': Number(4)
    }
    res = Machine(exp, exp_env).run()
    print('exp:', exp, 'res:', res)

    assign_exp = Assign(Varible('x'),
                        Add(Varible('x'), Number(1)))
    assign_exp_env = {
        'x': Number(2)
    }
    assign_res = Machine(assign_exp, assign_exp_env).run()
    print('exp:', assign_exp, 'res:', assign_res)

    if_exp = If(Varible('x'),
                Assign('y', Number(1)),
                Assign('y', Number(2)))
    if_exp_env = {
        'x': Boolean(True)
    }
    if_res = Machine(if_exp, if_exp_env).run()
    print('exp:', if_exp, 'res:', if_res)

    if_exp_1 = If(Varible('x'),
                  Assign('y', Number(1)),
                  DoNothing())
    if_exp_1_env = {
        'x': Boolean(False)
    }
    if_res_1 = Machine(if_exp_1, if_exp_1_env).run()
    print('exp:', if_exp_1, 'res:', if_res_1)

    sequence_exp = Sequence(Assign('x', Add(Number(1), Number(1))),
                            Assign('y', Add(Varible('x'), Number(3))))
    sequence_exp_env = {}
    sequence_res = Machine(sequence_exp, sequence_exp_env).run()
    print('exp:', sequence_exp, 'res:', sequence_res)

    while_exp = While(LessThan(Varible('x'), Number(5)),
                      Assign('x', Multiply(Varible('x'), Number(3))))
    while_exp_env = {
        'x': Number(1)
    }
    while_res = Machine(while_exp, while_exp_env).run()
    print('exp:', while_exp, 'res:', while_res)
