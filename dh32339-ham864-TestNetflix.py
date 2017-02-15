#!/usr/bin/env python3

# -------
# imports
# -------
from Netflix import netflix_eval
from unittest import main, TestCase
from math import sqrt
from io import StringIO
from numpy import sqrt, square, mean, subtract

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase):

    # ----
    # eval
    # ----

    def test_eval_1(self):
        r = StringIO("9913:\n389134\n537789\n2319678\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "9913:\n3.34\n3.333\n2.787\nRMSE: 0.82\n")

    def test_eval_2(self):
        r = StringIO("9916:\n178302\n1079746\n284686\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "9916:\n3.358\n2.777\n2.761\nRMSE: 0.41\n")
    def test_eval_3(self):
        r = StringIO("9918:\n206657\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "9918:\n2.965\nRMSE: 0.96\n")

    def test_eval_4(self):
        r = StringIO("9939:\n2525823\n1427683\n1022378\n293697\n53679\n2159332\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "9939:\n2.057\n3.987\n2.257\n4.126\n2.919\n3.851\nRMSE: 1.09\n")



# ----
# main
# ----
if __name__ == '__main__':
    main()

""" #pragma: no cover
% coverage3 run --branch TestNetflix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out



% cat TestNetflix.out
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
Name             Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------
Netflix.py          27      0      4      0   100%
TestNetflix.py      13      0      0      0   100%
------------------------------------------------------------
TOTAL               40      0      4      0   100%

"""
