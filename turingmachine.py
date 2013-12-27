# turingmachine.py - implementation of the Turing machine model
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
"""Provides an implementation of the Turing machine model."""

#: Translation of left and right strings to -1 and +1 for use in computing the
#: next location of the read/write head of the Turing machine.
DIRECTION_CHANGE = {'L': -1, 'R': +1}


class TuringMachine(object):
    """An implementation of the Turing machine model.

    Once instantiated, the Turing machine can be executed by calling it, and it
    can be reset to its initial state by calling :meth:`reset`.

    `states` is a set of states. A "state" can be anything, but usually simple
    integers suffice.

    `initial_state` is the state of the machine before it starts reading
    symbols from an input string. This state must be a member of `states`. When
    :meth:`reset` is called, the state of the machine will be set to this
    state.

    `accept_states` is a set of states that will cause the machine to halt and
    accept (that is, return ``True``). This set must be a subset of `states`.

    `reject_states` is a set of states that will cause the machine to halt and
    reject (that is, return ``False``). This set must be a subset of `states`.

    `transition` is a two-dimensional dictionary specifying how the
    "configuration" of the machine (that is, the head location, state, and
    string) changes each time it reads from its input string. The dictionary is
    indexed first by state, then by symbol. Each entry in this two-dimensional
    dictionary must be a three-tuple, *(new_state, new_symbol, direction)*,
    where *new_state* is the next state in which the Turing machine will be,
    *new_symbol* is the symbol that will be written in the current location on
    the string, and *direction* is either ``'L'`` or ``'R'``, representing
    movement of the head left or right, repectively.

    """

    def __init__(self, states, initial_state, accept_states, reject_states,
                 transition, *args, **kw):
        self.states = states
        self.accept_states = accept_states
        self.reject_states = reject_states
        self.initial_state = initial_state
        self.current_state = self.initial_state
        self.transition = transition
        # we assume that all strings will be input with one blank on the left
        # and one blank on the right
        self.head_location = 1

    def reset(self):
        """Resets the Turing machine to its initial state and head location."""
        self.head_location = 1
        self.current_state = self.initial_state

    def __call__(self, string):
        """Runs the computer program specified by this Turing machine on
        `string`.

        `string` must be a Python string whose first and last characters are
        underscores (``'_'``). The underscore represents a blank on the
        theoretical infinite input tape, and denotes the left and right ends of
        the input string.

        The initial head location of the Turing machine is the left-most
        non-blank character of the string.

        Calling this Turing machine executes the program specified by its
        transition function and returns ``True`` if the Turing machine halts
        and accepts and ``False`` if the Turing machine halts and rejects.

        If you intend to call this Turing machine more than once, you must call
        :meth:`reset` after each invocation, in order to reset the state of the
        Turing machine to its initial state and the location of the read/write
        head to the left most non-blank character of the string.

        """
        # for the sake of brevity, rename some verbose instance variable
        h = self.head_location
        q = self.current_state
        # compute the new configuration from the transition function
        new_state, new_symbol, direction = self.transition[q][string[h]]
        # check for accepting or rejecting configurations
        if new_state in self.accept_states:
            return True
        if new_state in self.reject_states:
            return False
        # write the specified new symbol to the string; Python strings are
        # immutable, so we must create a new one
        new_string = string[:h] + new_symbol + string[h + 1:]
        # set the new state and head location
        self.current_state = new_state
        self.head_location += DIRECTION_CHANGE[direction]
        # continue executing the Turing machine with the new configuration
        return self(new_string)
