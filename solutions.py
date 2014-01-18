from turingmachine import L
from turingmachine import R
from turingmachine import TuringMachine

#: The Turing machine that does nothing and always accepts; this is only used
#: to provide students with code that runs.
DEFAULT = TuringMachine({0}, 0, 0, 1,
                        {0: {k: (0, k, R) for k in ('0', '1', '_')}})

#: Problem 1: construct a Turing machine that decides the language
#:
#:     L = { 0^2n 1^n | n is a natural number }
#:
machine1 = DEFAULT

#: Problem 2: construct a Turing machine that decides the language
#:
#:     L = { w b w^R | w is a binary string and b is a bit }
#:
machine2 = DEFAULT

#: Problem 3: construct a Turing machine that decides the language
#:
#:     L = { 0^i 1^j 0^k | i, j, and k are positive integers and i * j = k }
#:
machine3 = DEFAULT
