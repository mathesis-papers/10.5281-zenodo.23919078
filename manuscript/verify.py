import argparse
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path


def identity(size):
    return [[Fraction(row == column) for column in range(size)] for row in range(size)]


def linear(terms):
    size = len(terms[0][1])
    return [[sum(coefficient * matrix[row][column] for coefficient, matrix in terms)
             for column in range(size)] for row in range(size)]


def multiply(left, right):
    size = len(left)
    return [[sum(left[row][inner] * right[inner][column] for inner in range(size))
             for column in range(size)] for row in range(size)]


def trace(matrix):
    return sum(matrix[index][index] for index in range(len(matrix)))


def pair(left, right):
    return trace(multiply(left, right))


def verify():
    words = list(product(range(3), repeat=3))
    size = len(words)
    unit = identity(size)
    support = [[Fraction(row == column and len(set(words[row])) <= 2)
                for column in range(size)] for row in range(size)]
    constant = [len(set(word)) == 1 for word in words]
    ghz = [[Fraction(constant[row] and constant[column], 3)
            for column in range(size)] for row in range(size)]
    complement = linear([(1, unit), (-1, support)])
    witness = linear([(Fraction(1, 3), support), (-1, ghz)])
    metric = linear([(Fraction(2, 3), ghz), (Fraction(4, 3), support),
                     (-Fraction(4, 3), ghz), (1, complement)])
    inverse = linear([(Fraction(3, 2), ghz), (Fraction(3, 4), support),
                      (-Fraction(3, 4), ghz), (1, complement)])
    noisy = linear([(Fraction(1, 72), unit), (Fraction(5, 8), ghz)])
    amplitudes = [4 if word == (0, 0, 0) else 1 if len(set(word)) == 1 else 0
                  for word in words]
    test_state = [[Fraction(amplitudes[row] * amplitudes[column], 18)
                   for column in range(size)] for row in range(size)]
    assert multiply(support, support) == support
    assert multiply(ghz, ghz) == ghz
    assert multiply(support, ghz) == ghz
    assert multiply(metric, inverse) == unit
    assert metric == linear([(Fraction(10, 9), unit), (Fraction(2, 3), witness),
                             (-Fraction(1, 9), complement)])
    assert trace(support) == 21 and trace(complement) == 6
    assert trace(noisy) == 1 and trace(test_state) == 1
    assert pair(noisy, witness) == pair(test_state, witness) == -Fraction(1, 3)
    assert pair(noisy, complement) == Fraction(1, 12)
    assert pair(test_state, ghz) == Fraction(2, 3)
    assert pair(test_state, support) == 1
    lower = -Fraction(2, 3) * pair(noisy, witness) + Fraction(1, 9) * pair(noisy, complement) - Fraction(1, 9)
    assert lower == Fraction(13, 108)
    assert lower - Fraction(1, 9) == Fraction(1, 108)
    ranks = []
    for dimension in range(3, 6):
        for parties in range(3, 7):
            counted = sum(len(set(word)) <= 2 for word in product(range(dimension), repeat=parties))
            formula = dimension + comb(dimension, 2) * (2 ** parties - 2)
            assert counted == formula < dimension ** parties
            ranks.append({'n': parties, 'd': dimension, 'rank': counted})
    scalar_cases = 0
    for dimension in range(3, 41):
        previous = dimension - 1
        polynomial = dimension ** 2 - 3 * dimension + 3
        slope = Fraction(previous, dimension * (dimension - 2))
        offset = Fraction(1, dimension ** 2 * (dimension - 2))
        eigen_a = Fraction(previous, dimension)
        eigen_b = Fraction(previous ** 2, dimension * (dimension - 2))
        witness_mean = -Fraction(2 * dimension - 3, dimension * polynomial)
        entanglement = Fraction(1, previous ** 3 + 1)
        assert 1 / eigen_a + previous / eigen_b == dimension
        assert eigen_b - eigen_a == slope
        assert eigen_b == 1 + offset + slope / dimension
        assert eigen_a == 1 + offset - slope * Fraction(previous, dimension)
        assert -slope * witness_mean - offset == entanglement
        norm = previous ** 4 + previous
        assert Fraction((previous ** 2 + previous) ** 2, dimension * norm) == Fraction(previous, polynomial)
        assert Fraction(previous, norm) == entanglement
        for parties in range(3, 13):
            ambient = dimension ** parties
            rank = dimension + comb(dimension, 2) * (2 ** parties - 2)
            growth = Fraction(previous, dimension) + Fraction(rank, dimension * ambient) - Fraction(1, ambient)
            noise = Fraction((dimension - 2) ** 2, polynomial) / growth
            assert 0 < noise < 1
            assert -Fraction(previous, dimension) + noise * growth == witness_mean
            assert offset * noise * (1 - Fraction(rank, ambient)) > 0
            scalar_cases += 1
    assert Fraction(27, 74) < Fraction(3, 8) < Fraction(9, 22)
    assert -Fraction(1, 3) + Fraction(74, 81) * Fraction(27, 74) == 0
    assert Fraction(1, 9) - Fraction(22, 81) * Fraction(9, 22) == 0
    return {
        'status': 'passed',
        'arithmetic': 'exact rational arithmetic with Python standard library',
        'matrix_dimension': size,
        'base_case': {'n': 3, 'd': 3, 'p': '3/8', 'witness_bound': '1/9',
                      'roof_lower_bound': str(lower), 'certified_gap': '1/108'},
        'finite_support_enumerations': ranks,
        'scalar_identity_checks': {'d_min': 3, 'd_max': 40, 'n_min': 3,
                                   'n_max': 12, 'cases': scalar_cases},
        'written_proof': 'note.tex: Theorem 1 covers every n,d >= 3; Corollary 1 covers the three-qutrit noise interval.',
        'lean_declaration': 'D5.S3.Quantum.Entanglement.Witness.NoisyGhzWitnessBoundGap.result',
        'lean_statement_scope': 'Negation of universal equality, via the three-qutrit bounds 1/9 and 13/108.',
    }


def main():
    parser = argparse.ArgumentParser(description='Check rational identities and finite support ranks for the noisy-GHZ gap.')
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    encoded = json.dumps(verify(), indent=2) + '\n'
    if arguments.output:
        arguments.output.write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
