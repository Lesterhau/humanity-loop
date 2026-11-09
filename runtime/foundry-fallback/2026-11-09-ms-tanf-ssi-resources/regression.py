#!/usr/bin/env python3
"""Exact-source, isolated PolicyEngine-US #10516 resource regression.

Runs the original and candidate class bodies reconstructed from the companion
unified diff against synthetic numpy-backed entity mocks. No PolicyEngine
package or network needed; this is NOT full simulation/YAML/CI validation.
Run: python regression.py (requires numpy)
"""
from pathlib import Path
from types import SimpleNamespace
import unittest
import numpy as np

PATCH = Path(__file__).with_name('candidate.patch').read_text()


def reconstruct():
    sections = []
    original = candidate = None
    for line in PATCH.splitlines(keepends=True):
        if line.startswith('--- '):
            if original is not None:
                sections.append((''.join(original), ''.join(candidate)))
            original, candidate = [], []
        elif line.startswith(('+++ ', '@@ ')):
            continue
        elif original is not None:
            if line.startswith((' ', '-')):
                original.append(line[1:])
            if line.startswith((' ', '+')):
                candidate.append(line[1:])
    sections.append((''.join(original), ''.join(candidate)))
    return sections


class Variable: pass
class Person: pass
class SPMUnit: pass
class StateCode: MS = 'MS'
MONTH = 'month'


def load(source, name):
    scope = dict(Variable=Variable, Person=Person, SPMUnit=SPMUnit,
                 StateCode=StateCode, MONTH=MONTH, where=np.where)
    exec(source.replace('from policyengine_us.model_api import *', ''), scope)
    return scope[name]


SOURCES = reconstruct()
assert len(SOURCES) == 2
Original = load(SOURCES[0][0], 'ms_tanf_resources_eligible')
Candidate = load(SOURCES[0][1], 'ms_tanf_resources_eligible')
Member = load(SOURCES[1][1], 'ms_tanf_is_assistance_unit_member')


class Members:
    def __init__(self, rows): self.rows = rows
    def __call__(self, name, period):
        if name == 'ms_tanf_is_assistance_unit_member':
            return Member.formula(self, period, None)
        return np.array([r.get(name, 0) for r in self.rows])


class Unit:
    def __init__(self, rows, aggregate=None):
        self.members = Members(rows)
        self.aggregate = aggregate if aggregate is not None else sum(
            r.get('bank_account_assets', 0) + r.get('stock_assets', 0)
            + r.get('bond_assets', 0) for r in rows)
    def __call__(self, name, period):
        assert name == 'spm_unit_cash_assets'
        return self.aggregate
    def sum(self, a): return np.sum(a)


PERIOD = SimpleNamespace(this_year='2026')
PARAMS = lambda p: SimpleNamespace(gov=SimpleNamespace(states=SimpleNamespace(
    ms=SimpleNamespace(dhs=SimpleNamespace(tanf=SimpleNamespace(
        resources=SimpleNamespace(limit=2000)))))))


def row(ssi=0, reported=False, bank=0, stock=0, bonds=0):
    return dict(ssi=ssi, receives_ssi=reported, bank_account_assets=bank,
                stock_assets=stock, bond_assets=bonds)


def calc(cls, rows, aggregate=None):
    return bool(cls.formula(Unit(rows, aggregate), PERIOD, PARAMS))


class TestSSIResources(unittest.TestCase):
    def test_member_mask(self):
        mask = Member.formula(Members([row(), row(ssi=900),
                                      row(reported=True), row()]), PERIOD, None)
        self.assertEqual(mask.tolist(), [True, False, False, True])

    def test_cases(self):
        cases = [
            ('nonssi_1500', [row(bank=1500), row()], None, True, False),
            ('nonssi_2500', [row(bank=2500), row()], None, False, False),
            ('ssi_parent_2600', [row(ssi=900, bank=2600), row()], None, True, True),
            ('ssi_child_stock_3000', [row(bank=200), row(ssi=800, stock=3000)], None, True, True),
            ('reported_ssi_bonds', [row(bank=100), row(reported=True, bonds=3000)], None, True, True),
            ('included_at_limit', [row(bank=1900, stock=100), row(ssi=850, bank=10000)], None, True, True),
            ('included_over_limit', [row(bank=1900, stock=100.02), row(ssi=850, bank=10000)], None, False, False),
            ('unattributed_override', [row(bank=100), row(ssi=800, bank=2600)], 5000, False, False),
            ('aggregate_only_3000', [row(), row()], 3000, False, False),
            ('nonssi_exact_limit', [row(bank=2000)], None, True, False),
            ('nonssi_over_limit', [row(bank=2000.02)], None, False, False),
        ]
        for name, rows, aggregate, expected, original_differs in cases:
            with self.subTest(name=name):
                got = calc(Candidate, rows, aggregate)
                self.assertEqual(got, expected)
                self.assertEqual(calc(Original, rows, aggregate) != got, original_differs)


if __name__ == '__main__': unittest.main(verbosity=2)
