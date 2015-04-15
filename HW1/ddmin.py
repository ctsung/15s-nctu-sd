#!/usr/bin/env python
# $Id: ddmin.py,v 2.2 2005/05/12 22:01:18 zeller Exp $

from split import split
from listsets import listminus
import re
import test
import sys
import os

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

def ddmin(circumstances, test):
    """Return a sublist of CIRCUMSTANCES that is a relevant configuration
       with respect to TEST."""
    n = 2
    while len(circumstances) >= 2:
        subsets = split(circumstances, n)

        some_complement_is_failing = 0
        for subset in subsets:
            complement = listminus(circumstances, subset)

            file = open('complement.xml', 'w')
            for c in complement:
                file.write(c[1])
            file.close()
            
            if test('complement.xml') == FAIL:
                circumstances = complement
                n = max(n - 1, 2)
                some_complement_is_failing = 1
                break

        if not some_complement_is_failing:
            if n == len(circumstances):
                break
            n = min(n * 2, len(circumstances))

    os.remove('complement.xml')
    return circumstances



if __name__ == "__main__":
    circumstances = []
    simplified_input = ''

    def string_to_list(s):
        c = []
        for i in range(len(s)):
            c.append((i, s[i]))
        return c
    
    circumstances = string_to_list(open(sys.argv[1]).read())
    result = ddmin(circumstances, test.test)
    
    for c in result:
        simplified_input += c[1]
    print simplified_input
