from the_simplest_computers.finite_automata import NFARulebook, NFADesign, FARule


class State:
    def __init__(self, state_name):
        self.state_name = state_name

    def __repr__(self):
        return f"{self.state_name}"


class Pattern:
    precedence = None

    def to_nfa_design(self):
        raise NotImplemented

    def bracket(self, out_precedence):
        if self.precedence < out_precedence:
            return f"({self})"
        else:
            return f"{self}"

    def matches(self, string):
        return self.to_nfa_design().accepts(string)


class Empty(Pattern):
    precedence = 3

    def __repr__(self):
        return ''

    def to_nfa_design(self):
        state_obj = State('empty')
        rulebook = NFARulebook([])
        return NFADesign(state_obj, {state_obj}, rulebook)


class Literal(Pattern):
    precedence = 3

    def __init__(self, character):
        self.character = character

    def __repr__(self):
        return self.character

    def to_nfa_design(self):
        start_state = State('literal_start')
        accept_state = State('literal_accept')
        rule = FARule(start_state, self.character, accept_state)
        rulebook = NFARulebook([rule])
        return NFADesign(start_state, {accept_state}, rulebook)


class Concatenate(Pattern):
    precedence = 1

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        repr_l = [i.bracket(self.precedence) for i in [self.first, self.second]]
        return f"{''.join(repr_l)}"

    def to_nfa_design(self):
        first_nfa_design = self.first.to_nfa_design()
        second_nfa_design = self.second.to_nfa_design()

        start_state = first_nfa_design.start_state
        accept_states = second_nfa_design.accept_states

        rules = first_nfa_design.rulebook.rules + second_nfa_design.rulebook.rules
        extra_rules = [FARule(state, None, second_nfa_design.start_state)
                       for state in first_nfa_design.accept_states]
        rulebook = NFARulebook(rules + extra_rules)

        return NFADesign(start_state, accept_states, rulebook)


class Choose(Pattern):
    precedence = 0

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        repr_l = [i.bracket(self.precedence) for i in [self.first, self.second]]
        return f"{'|'.join(repr_l)}"

    def to_nfa_design(self):
        first_nfa_design = self.first.to_nfa_design()
        second_nfa_design = self.second.to_nfa_design()

        start_state = State('choose')
        accept_states = first_nfa_design.accept_states | second_nfa_design.accept_states

        rules = first_nfa_design.rulebook.rules + second_nfa_design.rulebook.rules
        extra_rules = [FARule(start_state, None, nfa_design.start_state)
                       for nfa_design in [first_nfa_design, second_nfa_design]]
        rulebook = NFARulebook(rules + extra_rules)

        return NFADesign(start_state, accept_states, rulebook)


class Repeat(Pattern):
    precedence = 2

    def __init__(self, pattern):
        self.pattern = pattern

    def __repr__(self):
        return self.pattern.bracket(self.precedence) + '*'

    def to_nfa_design(self):
        pattern_nfa_design = self.pattern.to_nfa_design()

        start_state = State('repeat')
        accept_states = pattern_nfa_design.accept_states | {start_state}

        rules = pattern_nfa_design.rulebook.rules
        extra_rules = ([FARule(accept_state, None, pattern_nfa_design.start_state)
                        for accept_state in pattern_nfa_design.accept_states]
                       + [FARule(start_state, None, pattern_nfa_design.start_state)])
        rulebook = NFARulebook(rules + extra_rules)

        return NFADesign(start_state, accept_states, rulebook)


if __name__ == '__main__':
    pattern = Repeat(Choose(Concatenate(Literal('a'),
                                        Literal('b')),
                            Literal('a')))
    print(pattern)

    # Empty Literal nfa_design
    nfa_design = Empty().to_nfa_design()
    print('Empty',
          nfa_design.accepts(''),
          nfa_design.accepts('a'))

    nfa_design = Literal('a').to_nfa_design()
    print('Literal',
          nfa_design.accepts(''),
          nfa_design.accepts('a'),
          nfa_design.accepts('b'))

    print(Empty().matches('a'),
          Literal('a').matches('a'))

    # Concatenate
    pattern = Concatenate(Literal('a'), Literal('b'))
    print(pattern)
    print(pattern.matches('a'),
          pattern.matches('ab'),
          pattern.matches('abc'))

    pattern = Concatenate(Literal('a'),
                          Concatenate(Literal('b'),
                                      Literal('c')))
    print(pattern.matches('a'),
          pattern.matches('ab'),
          pattern.matches('abc'))

    # Choose
    pattern = Choose(Literal('a'), Literal('b'))
    print(pattern.matches('a'),
          pattern.matches('b'),
          pattern.matches('c'))

    # Repeat
    pattern = Repeat(Literal('a'))
    print(pattern)
    print(pattern.matches(''),
          pattern.matches('a'),
          pattern.matches('aaaa'),
          pattern.matches('b'))

    pattern = Repeat(Concatenate(Literal('a'),
                                 Choose(Empty(),
                                        Literal('b'))))
    print(pattern)
    print(pattern.matches(''),
          pattern.matches('a'),
          pattern.matches('ab'),
          pattern.matches('aba'),
          pattern.matches('abab'),
          pattern.matches('abaab'),
          pattern.matches('abba'))
