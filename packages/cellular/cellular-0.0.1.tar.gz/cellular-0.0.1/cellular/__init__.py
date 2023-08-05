import argparse
from time import sleep

from .main import CellularAutomaton, BORDER


def main():
    parser = argparse.ArgumentParser(description='Cellular Automaton')
    parser.add_argument('-r', '--rule', type=int, default=170, help='Evaluation rules.', choices=range(256))
    parser.add_argument('-b', '--border', default='fixed', help='Border type.', choices=BORDER.keys())
    parser.add_argument('-i', '--interval', default=0.1, type=float, help='Interval between evaluation.')
    parser.add_argument('-n', type=int, default=100, help='How much steps')
    parser.add_argument('-l', '--length', type=int, help='Length of sequence')

    args = parser.parse_args()

    ca = CellularAutomaton(rule=args.rule, border=args.border, length=args.length)
    for _ in range(args.n):
        ca.evaluate()
        print(ca.display())
        sleep(args.interval)
