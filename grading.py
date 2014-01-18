#!/usr/bin/env python3

import logging
import sys

from solutions import machine1
from solutions import machine2
from solutions import machine3
from turingmachine import logger as tm_logger

# Create and configure the logger which logs debugging information by default.
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
if len(sys.argv) >= 2 and sys.argv[1] == '-v':
    logger.setLevel(level=logging.DEBUG)
    tm_logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)
    tm_logger.setLevel(level=logging.INFO)


def test_machine(machine, should_accept, should_reject):
    # count the number of strings that the machine correctly accepts
    score = 0
    for w in should_accept:
        machine.reset()
        try:
            # add blanks before and after the string
            assert machine('_' + w + '_')
            msg = '  ✓ Accepted "{}".'.format(w)
            logger.debug(msg)
            score += 1
        except AssertionError:
            msg = '  ✗ Rejected "{}" but should have accepted.'.format(w)
            logger.debug(msg)
        except Exception as e:
            msg = '  ✗ ' + str(exception)
            logger.error(msg)
    # count the number of strings that the machine correctly rejects
    for w in should_reject:
        machine.reset()
        try:
            # add blanks before and after the string
            assert not machine('_' + w + '_')
            msg = '  ✓ Rejected "{}".'.format(w)
            logger.debug(msg)
            score += 1
        except AssertionError:
            msg = '  ✗ Accepted "{}" but should have rejected.'.format(w)
            logger.debug(msg)
        except Exception as e:
            msg = '  ✗ ' + str(exception)
            logger.error(msg)
    return score


def main():
    logger.info('Test for L = { 0^2n 1^n | n is a natural number }.')
    should_accept = ['0' * 2 * n + '1' * n for n in range(5)]
    should_reject = ['0', '01', '101', '0010', '1111']
    max_score = len(should_accept) + len(should_reject)
    score = test_machine(machine1, should_accept, should_reject)
    logger.info('-' * 50)
    logger.info('Total score: {}/{}'.format(score, max_score))

    logger.info('')
    logger.info('Test for L = { w b w^R | w is a binary string'
                ' and b is a bit }.')
    should_accept = ['1', '000', '010', '11011', '1110111']
    should_reject = ['', '00', '0110', '110011', '0010']
    max_score = len(should_accept) + len(should_reject)
    score = test_machine(machine2, should_accept, should_reject)
    logger.info('-' * 50)
    logger.info('Total score: {}/{}'.format(score, max_score))

    logger.info('')
    logger.info('Test for L = { 0^i 1^j 0^k | i, j, and k are'
                ' positive integers and i * j = k }.')
    should_accept = ['010', '01111100000', '00111000000', '000111000000000']
    should_reject = ['', '011', '0011100000', '0001110000000001']
    max_score = len(should_accept) + len(should_reject)
    score = test_machine(machine3, should_accept, should_reject)
    logger.info('-' * 50)
    logger.info('Total score: {}/{}'.format(score, max_score))

if __name__ == '__main__':
    main()
