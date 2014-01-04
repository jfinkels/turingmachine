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
import logging

# To make debugging messages visible, uncomment the following line.
#logging.basicConfig(level=logging.DEBUG)

#: Represents a movement of the read/write head of the Turing machine to the
#: left.
L = -1

#: Represents a movement of the read/write head of the Turing machine to the
#: right.
R = +1


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

    `accept_state` is the state that will cause the machine to halt and accept
    (that is, return ``True``). This set must be a member of `states`.

    `reject_state` is the state that will cause the machine to halt and reject
    (that is, return ``False``). This set must be a member of `states`.

    `transition` is a two-dimensional dictionary specifying how the
    "configuration" of the machine (that is, the head location, state, and
    string) changes each time it reads from its input string. The dictionary is
    indexed first by state, then by symbol. Each entry in this two-dimensional
    dictionary must be a three-tuple, *(new_state, new_symbol, direction)*,
    where *new_state* is the next state in which the Turing machine will be,
    *new_symbol* is the symbol that will be written in the current location on
    the string, and *direction* is either :data:`L` or :data:`R`, representing
    movement of the head left or right, repectively.

    The transition dictionary need not have an entry for the accept and reject
    states. For example, the accept and reject states need not be in
    `transition`, because the implementation of :meth:`__call__` checks if this
    Turing machine has entered one of these states and immediately halts
    execution.

    Altohugh they would otherwise be necessary in the formal mathematical
    definition of a Turing machine, this class requires the user to specify
    neither the input alphabet nor the tape alphabet.

    """

    def __init__(self, states, initial_state, accept_state, reject_state,
                 transition, *args, **kw):
        self.states = states
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.initial_state = initial_state
        self.current_state = self.initial_state
        self.transition = transition
        # we assume that all strings will be input with one blank on the left
        # and one blank on the right
        self.head_location = 1

    def _log_state(self, string):
        """Logs a visual representation of the current head location, state,
        and contents of the tape of this Turing machine.

        For example, if the Turing machine has ``'_010_'`` on its input tape
        (that is, if `string` is ``'_010_'``), is in state ``4``, and has
        read/write head at the location of the ``1`` symbol, this method would
        log the following messages, one line at a time.

            _010_
              ^
              4

        The caret represents the current location of the read/write head, and
        the number beneath it represents the current state of the machine.

        This method should be called from :meth:`__call__`, during the
        execution of the Turing machine on a particular string.

        """
        h = self.head_location
        q = self.current_state
        logging.debug('')
        logging.debug(string)
        logging.debug(' ' * h + '^')
        logging.debug(' ' * h + str(q))

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
        # If the head has moved too far to the left or right, add a blank to
        # the current string in the appropriate location. If a blank is added
        # to the left, the head location must be incremented, since the string
        # has now essentially been shifted right by one cell.
        if self.head_location < 0:
            string = '_' + string
            self.head_location += 1
        elif self.head_location >= len(string):
            string += '_'
        self._log_state(string)
        # for the sake of brevity, rename some verbose instance variable
        h = self.head_location
        q = self.current_state
        # compute the new configuration from the transition function
        #
        # TODO raise an exception if string[h] contains an unknown symbol
        new_state, new_symbol, direction = self.transition[q][string[h]]
        # check for accepting or rejecting configurations
        if new_state == self.accept_state:
            return True
        if new_state == self.reject_state:
            return False
        # write the specified new symbol to the string; Python strings are
        # immutable, so we must create a new one
        new_string = string[:h] + new_symbol + string[h + 1:]
        # set the new state and head location
        self.current_state = new_state
        # direction is either L or R, which are defined to be -1 and +1
        self.head_location += direction
        # continue executing the Turing machine with the new configuration
        return self(new_string)

    def reset(self):
        """Resets the Turing machine to its initial state and head location.

        This method should be called before each invocation of this Turing
        machine.

        """
        self.head_location = 1
        self.current_state = self.initial_state
