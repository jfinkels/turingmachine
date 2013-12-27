# test_turingmachine.py - tests for turingmachine.py
#
# Copyright 2013 Jeffrey Finkelstein.
#
# This file is part of turingmachine.
#
# turingmachine is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# turingmachine is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# turingmachine.  If not, see <http://www.gnu.org/licenses/>.
"""Provides tests for :mod:`turingmachine`."""

import unittest

from turingmachine import TuringMachine


class TestTuringMachine(unittest.TestCase):

    def test_is_even(self):
        """Tests the execution of a Turing machine that computes whether a
        binary string represents an even number.

        """
        states = set(range(4))
        initial_state = 0
        accept_states = {2}
        reject_states = {3}
        transition = {
            # this state represents moving right all the way to the end
            0: {
                '0': (0, '0', 'R'),
                '1': (0, '1', 'R'),
                '_': (1, '_', 'L'),
                },
            # this state represents looking at the rightmost symbol
            1: {
                '0': (2, '0', 'L'),
                '1': (3, '1', 'L'),
                '_': (3, '_', 'R'),
                },
            # this is the accept state
            2: {
                '0': (2, '0', 'L'),
                '1': (2, '1', 'L'),
                '_': (2, '_', 'L'),
                },
            # this is the reject state
            3: {
                '0': (3, '0', 'L'),
                '1': (3, '1', 'L'),
                '_': (3, '_', 'L'),
                }
            }
        is_even = TuringMachine(states, initial_state, accept_states,
                                reject_states, transition)
        for s in '_011010_', '_0_', '_1100010_':
            assert is_even(s)
            is_even.reset()
        for s in '_1101_', '_1_', '__', '_01001_':
            assert not is_even(s)
            is_even.reset()
