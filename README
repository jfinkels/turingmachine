# Turing machine simulator #

This package contains a Turing machine simulator for Python 3.

## Getting the code ##

Run

    git clone git@github.com:jfinkels/turingmachine

## Testing the code ##

Run

    python3 -m unittest test_turingmachine

## Using the code ##

The `turingmachine` module contains a `TuringMachine` class, whose instances
are (simulated) Turing machines. The example below creates a Turing machine
that accepts if and only if its input string has an odd number of ones.

    from turingmachine import TuringMachine

    states = {0, 1, 2, 3}
    initial_state = 0
    accept_state = 2
    reject_state = 3
    transitions = {
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

    parity = TuringMachine(states, initial_state, accept_state, reject_state
                           transitions)

    assert parity('_010101_')
    assert not parity('_010100_')

Inputs to the Turing machine must have underscore (`_`) symbols as the first
and last characters, so that the Turing machine can easily recognize the
beginning and end of its input.

## Copyright ##

Copyright 2014 Jeffrey Finkelstein.

This software is distributed under the terms of the GNU General Public License
version 3, or (at your option) any later version.

See the `LICENSE` file for more information.

## Contact ##

Jeffrey Finkelstein <jeffrey.finkelstein@gmail.com>
