import os
from random import randint

def terminal_size():
    row, col = os.popen('stty size', 'r').read().split()
    return int(row), int(col)


BORDER = {
    'fixed': lambda seq, i: 0,
    'periodic': lambda seq, i: seq[-1] if i == 0 else seq[0],
    'insulation': lambda seq, i: seq[i],
    'reflext': lambda seq, i: seq[min(1, len(seq))] if i == 0 else seq[min(-2, len(seq) - 1)]
}


class CellularAutomaton:
    def __init__(self, length=None, rule=170, border='fixed'):
        if length is None:
            _, col = terminal_size()
            self.sequence = [randint(0, 1) for _ in range(col)]
        else:
            self.sequence = [randint(0, 1) for _ in range(length)]

        assert self.sequence
        assert 0 <= rule < 256
        assert border in BORDER

        self.len = len(self.sequence)
        self.rule = rule
        self.power = self.parse_rule()
        self.border = BORDER[border]


    def parse_rule(self):
        power = [0] * 8
        n = self.rule
        for i in range(7, -1, -1):
            if n >= 2 ** i:
                power[i] = 1
                n -= 2 ** i

        return power


    def eval(self, neighbor):
        return self.power[int('{}{}{}'.format(*neighbor), 2)]


    def evaluate(self):
        next_gen = [0] * self.len
        next_gen[0] = self.eval([self.border(self.sequence, 0)] + self.sequence[:2])
        next_gen[-1] = self.eval(self.sequence[:2] + [self.border(self.sequence, -1)])
        for i in range(1, self.len - 1):
            next_gen[i] = self.eval(self.sequence[i-1:i+2])

        self.sequence = next_gen


    def display(self):
        return ''.join(['█' if s == 1 else ' ' for s in self.sequence])
