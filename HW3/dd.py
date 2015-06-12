#!/usr/bin/env python
# $Id: dd.py,v 2.4 2005/04/28 20:37:11 zeller Exp $

import split
from listsets import listminus, listunion
import re
import test
import sys
import os

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

def dd(c_pass, c_fail, test, splitter = None):
    """Return a triple (DELTA, C_PASS', C_FAIL') such that
       - C_PASS subseteq C_PASS' subset C_FAIL' subseteq C_FAIL holds
       - DELTA = C_FAIL' - C_PASS' is a minimal difference
         between C_PASS' and C_FAIL' that is relevant with respect to TEST."""

    if splitter is None:
        splitter = split.split

    n = 2
    while 1:
        delta = listminus(c_fail, c_pass)

        if n > len(delta):
            # No further minimizing
            return (delta, c_pass, c_fail)

        deltas = splitter(delta, n)

        offset = 0
        j = 0
        while j < n:
            i = (j + offset) % n
            next_c_pass = listunion(c_pass, deltas[i])
            next_c_fail = listminus(c_fail, deltas[i])

            file = open('next_c_pass.xml', 'w')
            for c in next_c_pass:
                file.write(c[1])
            file.close()

            file = open('next_c_fail.xml', 'w')
            for c in next_c_pass:
                file.write(c[1])
            file.close()

            if test('next_c_fail.xml') == FAIL and n == 2:
                c_fail = next_c_fail
                n = 2
                offset = 0
                break
            elif test('next_c_fail.xml') == PASS:
                c_pass = next_c_fail
                n = 2
                offset = 0
                break
            elif test('next_c_pass.xml') == FAIL:
                c_fail = next_c_pass
                n = 2
                offset = 0
                break
            elif test('next_c_fail.xml') == FAIL:
                c_fail = next_c_fail
                n = max(n - 1, 2)
                offset = i
                break
            elif test('next_c_pass.xml') == PASS:
                c_pass = next_c_pass
                n = max(n - 1, 2)
                offset = i
                break
            else:
                j = j + 1

        os.remove('next_c_pass.xml')
        os.remove('next_c_fail.xml')

        if j >= n:
            if n >= len(delta):
                return (delta, c_pass, c_fail)
            else:
                n = min(len(delta), n * 2)

if __name__ == "__main__":
    def string_to_list(s):
        c = []
        for i in range(len(s)):
            c.append((i, s[i]))
        return c
    
    c_pass = []
    c_fail = string_to_list(open(sys.argv[1]).read())
    
    result = dd(c_pass, c_fail, test.test)
