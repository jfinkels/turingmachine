# test_turingmachine.py - tests for turingmachine.py
#
# Copyright 2014 Jeffrey Finkelstein.
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

from collections import defaultdict
import unittest

from turingmachine import L
from turingmachine import R
from turingmachine import TuringMachine


class TestTuringMachine(unittest.TestCase):

    def test_move_left_and_right(self):
        """Tests the execution of a Turing machine that simply moves left and
        right.

        """
        states = set(range(17))
        initial_state = 0
        accept_state = 15
        reject_state = 16
        # Move left five cells then move right ten cells. Always accept.
        transition = defaultdict(dict)
        for state in range(5):
            for symbol in '0', '1', '_':
                transition[state][symbol] = (state + 1, symbol, L)
        for state in range(5, 15):
            for symbol in '0', '1', '_':
                transition[state][symbol] = (state + 1, symbol, R)
        move_left_right = TuringMachine(states, initial_state, accept_state,
                                        reject_state, transition)
        for s in '', '010', '000000':
            assert move_left_right('_' + s + '_')
            move_left_right.reset()

    def test_is_even(self):
        """Tests the execution of a Turing machine that computes whether a
        binary string represents an even number.

        """
        states = set(range(4))
        initial_state = 0
        accept_state = 2
        reject_state = 3
        transition = {
            # this state represents moving right all the way to the end
            0: {
                '0': (0, '0', R),
                '1': (0, '1', R),
                '_': (1, '_', L),
                },
            # this state represents looking at the rightmost symbol
            1: {
                '0': (accept_state, '0', L),
                '1': (reject_state, '1', L),
                '_': (reject_state, '_', R),
                }
            #2: {}  # this is the accept state
            #3: {}  # this is the reject state
            }
        is_even = TuringMachine(states, initial_state, accept_state,
                                reject_state, transition)
        for s in '011010', '0', '1100010':
            assert is_even('_' + s + '_')
            is_even.reset()
        for s in '1101', '1', '', '01001':
            assert not is_even('_' + s + '_')
            is_even.reset()

    def test_parity(self):
        """Tests the execution of a Turing machine that computes the parity of
        a binary string, that is, whether the number of ones in the binary
        strings is odd.

        """
        states = range(4)
        initial_state = 0
        accept_state = 2
        reject_state = 3
        # begin in pre-reject state
        # repeat:
        #   if reading a 1:
        #     if in pre-accept state, move to pre-reject state
        #     if in pre-reject state, move to pre-accept state
        #   move right
        # if in pre-accept, accept
        # if in pre-reject, reject
        transition = {
            # this state represents having read an even number of ones
            0: {
                '0': (0, '0', R),
                '1': (1, '1', R),
                '_': (reject_state, '_', L),
                },
            # this state represents having read an odd number of ones
            1: {
                '0': (1, '0', R),
                '1': (0, '1', R),
                '_': (accept_state, '_', R),
                }
            }
        parity = TuringMachine(states, initial_state, accept_state,
                               reject_state, transition)
        for s in '011010', '1', '1101011':
            assert parity('_' + s + '_')
            parity.reset()
        for s in '1001', '0', '', '001001':
            assert not parity('_' + s + '_')
            parity.reset()

    def test_is_palindrome(self):
        """Tests the execution of a Turing machine that computes whether a
        binary string is a palindrome.

        """
        states = range(10)
        initial_state = 0
        accept_state = 8
        reject_state = 9
        # This is a description of the implementation of the Turing machine
        # that decides whether a binary string is a palindrome.
        #
        # repeat the following steps:
        #   read a symbol
        #   if _: accept
        #   if 0:
        #     write blank
        #     move right
        #     if _: accept (because it is a single 0)
        #     otherwise repeatedly move right to end
        #     at terminal blank move left
        #     if 1: reject
        #     else: write blank
        #   if 1:
        #     write blank
        #     move right
        #     if _: accept (because it is a single 1)
        #     repeatedly move right to end
        #     at terminal blank move left
        #     if 0: reject
        #     else: write blank
        #   repeatedly move left to end
        transition = {
            # read the first symbol
            0: {
                '0': (6, '_', R),
                '1': (7, '_', R),
                '_': (accept_state, '_', R)
                },
            # string starts with 0; move repeatedly right
            1: {
                '0': (1, '0', R),
                '1': (1, '1', R),
                '_': (3, '_', L)
                },
            # string starts with 1; move repeatedly right
            2: {
                '0': (2, '0', R),
                '1': (2, '1', R),
                '_': (4, '_', L)
                },
            # rightmost symbol should be a 0
            3: {
                '0': (5, '_', L),
                '1': (reject_state, '1', L),
                '_': (reject_state, '_', L)  # this situation is unreachable
                },
            # rightmost symbol should be a 1
            4: {
                '0': (reject_state, '0', L),
                '1': (5, '_', L),
                '_': (reject_state, '_', L)  # this situation is unreachable
                },
            # repeatedly move left to the beginning of the string
            5: {
                '0': (5, '0', L),
                '1': (5, '1', L),
                '_': (0, '_', R)
                },
            # check if there is only one symbol left
            6: {
                '0': (1, '0', R),
                '1': (1, '1', R),
                '_': (accept_state, '_', L)
                },
            # check if there is only one symbol left
            7: {
                '0': (2, '0', R),
                '1': (2, '1', R),
                '_': (accept_state, '_', L)
                }
            #7: {}  # this is the accept state
            #8: {}  # this is the reject state
            }
        is_palindrome = TuringMachine(states, initial_state, accept_state,
                                      reject_state, transition)
        for s in '', '0', '010', '111010111':
            assert is_palindrome('_' + s + '_')
            is_palindrome.reset()
        for s in '01', '110', '111100001':
            assert not is_palindrome('_' + s + '_')
            is_palindrome.reset()
