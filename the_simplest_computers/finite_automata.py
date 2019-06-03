from itertools import chain


class FARule:
    def __init__(self, status, character, next_status):
        self.status = status
        self.character = character
        self.next_status = next_status

    def __repr__(self):
        return f"FARule {self.status} -- {self.character} -> {self.next_status}"

    def applies_to(self, status, character):
        return self.status == status and self.character == character

    def follow(self):
        return self.next_status


class DFARulebook:
    def __init__(self, rules):
        self.rules = rules

    def __repr__(self):
        return f"{self.rules}"

    def next_state(self, state, character):
        return self.rule_for(state, character).follow()

    def rule_for(self, state, character):
        for rule in self.rules:
            if rule.applies_to(state, character):
                return rule


class DFA:
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return self.current_state in self.accept_states

    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state, character)

    def read_string(self, string):
        for i in string:
            self.read_character(i)


class DFADesign:
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def accepts(self, string):
        dfa = self.to_dfa()
        dfa.read_string(string)
        return dfa.accepting()


class NFARulebook:
    def __init__(self, rules):
        self.rules = rules

    def __repr__(self):
        return f"{self.rules}"

    def next_states(self, states: set, character):
        return set(chain(*[self.follow_rules_for(state, character) for state in states]))

    def follow_rules_for(self, state: set, character):
        return [rule.follow() for rule in self.rules_for(state, character)]

    def rules_for(self, state: set, character):
        return [rule for rule in self.rules if rule.applies_to(state, character)]

    def follow_free_moves(self, states: set):
        move_states = self.next_states(states, None)
        if move_states.issubset(states):
            return states
        else:
            return self.follow_free_moves(states | move_states)


class NFA:
    def __init__(self, current_states: set, accept_states: set, rulebook):
        self._current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def current_states(self):
        return self.rulebook.follow_free_moves(self._current_states)

    def accepting(self):
        return any(self.current_states & self.accept_states)

    def read_character(self, character):
        self._current_states = self.rulebook.next_states(self.current_states, character)

    def read_string(self, string: str):
        for i in string:
            self.read_character(i)


class NFADesign:
    def __init__(self, start_state, accept_states: set, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepts(self, string: str):
        nfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.accepting()

    def to_nfa(self):
        return NFA({self.start_state}, self.accept_states, self.rulebook)


if __name__ == '__main__':
    rules = [FARule(1, 'a', 2), FARule(1, 'b', 1),
             FARule(2, 'a', 2), FARule(2, 'b', 3),
             FARule(3, 'a', 3), FARule(3, 'b', 3)]
    rulebook = DFARulebook(rules)

    print(rulebook.next_state(1, 'a'),
          rulebook.next_state(1, 'b'),
          rulebook.next_state(2, 'b'))

    print(DFA(1, [1, 3], rulebook).accepting(),
          DFA(1, [3], rulebook).accepting())

    # read_character
    dfa = DFA(1, [3], rulebook)
    print(dfa.accepting())

    dfa.read_character('b')
    for i in range(3):
        dfa.read_character('a')
    dfa.read_character('b')

    print('read_character', dfa.accepting())

    # read_string
    dfa = DFA(1, [3], rulebook)
    print(dfa.accepting())
    dfa.read_string('baaab')
    print('read_string', dfa.accepting())

    # dfa_design
    dfa_design = DFADesign(1, [3], rulebook)
    print('dfa_design: ',
          dfa_design.accepts('a'),
          dfa_design.accepts('baa'),
          dfa_design.accepts('baba'))

    # nfa
    nfa_rules = [FARule(1, 'a', 1), FARule(1, 'b', 1), FARule(1, 'b', 2),
                 FARule(2, 'a', 3), FARule(2, 'b', 3),
                 FARule(3, 'a', 4), FARule(3, 'b', 4)]
    nfa_rulebook = NFARulebook(nfa_rules)

    print(nfa_rulebook.next_states({1}, 'b'),
          nfa_rulebook.next_states({1, 2}, 'a'),
          nfa_rulebook.next_states({1, 3}, 'b'))

    print(NFA({1}, {4}, nfa_rulebook).accepting(),
          NFA({1, 2, 4}, {4}, nfa_rulebook).accepting())

    # nfa read_character
    nfa = NFA({1}, {4}, nfa_rulebook)
    print(nfa.accepting())
    nfa.read_character('b')
    nfa.read_character('a')
    nfa.read_character('b')
    print('read_character', nfa.accepting())

    # nfa read_string
    nfa = NFA({1}, {4}, nfa_rulebook)
    print(nfa.accepting())
    nfa.read_string('bbbbb')
    print('read_string', nfa.accepting())

    # nfa_design
    nfa_design = NFADesign(1, {4}, nfa_rulebook)
    print('nfa_design: ',
          nfa_design.accepts('bab'),
          nfa_design.accepts('bbbbb'),
          nfa_design.accepts('bbabb'))

    nfa_free_move_rule = [FARule(1, None, 2), FARule(1, None, 4),
                          FARule(2, 'a', 3),
                          FARule(3, 'a', 2),
                          FARule(4, 'a', 5),
                          FARule(5, 'a', 6),
                          FARule(6, 'a', 4)]
    nfa_free_move_rulebook = NFARulebook(nfa_free_move_rule)
    print(nfa_free_move_rulebook.next_states({1}, None))

    # free_moves
    print(nfa_free_move_rulebook.follow_free_moves({1}))
    nfa_design = NFADesign(1, {2, 4}, nfa_free_move_rulebook)
    print(nfa_design.accepts('aa'),
          nfa_design.accepts('aaa'),
          nfa_design.accepts('aaaaa'),
          nfa_design.accepts('aaaaaa'))
