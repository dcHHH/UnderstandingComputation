class Number:
    def __init__(self, value):
        self.value = value

    def to_python(self):
        return repr(self.value)


class Boolean:
    def __init__(self, value):
        self.value = value

    def to_python(self):
        return repr(self.value)


class Varible:
    def __init__(self, name):
        self.name = name

    def to_python(self):
        return self.name


class DoNothing:
    @staticmethod
    def to_python():
        return ''


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_python(self):
        left = repr(self.left.to_python())
        right = repr(self.right.to_python())
        return f"eval({left}, globals()) + eval({right}, globals())"


class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_python(self):
        left = repr(self.left.to_python())
        right = repr(self.right.to_python())
        return f"eval({left}, globals()) * eval({right}, globals())"


class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_python(self):
        left = repr(self.left.to_python())
        right = repr(self.right.to_python())
        return f"eval({left}, globals()) < eval({right}, globals())"


class Assign:
    reducible = True

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def to_python(self):
        expression = repr(self.expression.to_python())
        return f"{self.name} = eval({expression}, globals())"


class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def to_python(self):
        condition = repr(self.condition.to_python())
        consequence = repr(self.consequence.to_python())
        alternative = repr(self.alternative.to_python())
        return f"if {condition}:\n    {consequence}\nelse:    {alternative}"


class Sequence:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def to_python(self):
        first = self.first.to_python()
        second = self.second.to_python()
        return f"{first}\n{second}"


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def to_python(self):
        condition = self.condition.to_python()
        body = self.body.to_python()
        return f"while {condition}:\n    {body}"


if __name__ == '__main__':
    print(eval(Number(23).to_python()))
    print(eval(Varible('x').to_python(), {'x': 23}))

    exp = LessThan(Add(Varible('x'), Number(2)),
                   Varible('y'))
    exp_env = {'x': 2, 'y': 5}
    res = eval(exp.to_python(), exp_env)
    print(res)

    # sequence
    seq_exp = Sequence(Assign('x', Add(Number(1), Number(1))),
                       Assign('y', Add(Varible('x'), Number(3))))
    seq_env = {}
    seq_res = exec(seq_exp.to_python(), seq_env)
    print(seq_res)
    print({k: v for k, v in seq_env.items() if not k == '__builtins__'})

    # while
    while_exp = While(LessThan(Varible('x'), Number(5)),
                      Assign('x', Multiply(Varible('x'), Number(3))))
    while_env = {'x': 1}
    while_res = exec(while_exp.to_python(), while_env)
    print(while_res)
    print({k: v for k, v in while_env.items() if not k == '__builtins__'})
