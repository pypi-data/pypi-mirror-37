##
# -*- coding: utf-8 -*-
#
# File:    PyWrapTestLibTests.py
# Author:  J. Westbrook
# Date:    18-Dec-2017
# Version: 0.001
#
# Updates:
#   3-Jan-2018  jdw integrate tests with package path -
#
##
"""
Test cases for basic class and enum wrapping using std::string and std::vector containers

"""
from __future__ import absolute_import

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import sys
import os
import unittest
import time

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


import wrap_pybind11.pywraptestlib as ptl
from wrap_pybind11.pywraptestlib import StringA
from wrap_pybind11.pywraptestlib import StringB
from wrap_pybind11.pywraptestlib import StringC
from wrap_pybind11.pywraptestlib import methodCombine1G, methodCombine2G, methodCombine3G


class pywraptestlibTests(unittest.TestCase):

    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__startTime = time.time()
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

    def testSimpleAccessorsA(self):
        """Test case - base class instantiation with ascii data
        """
        try:
            iVal = 100
            sA = StringA()
            sA.setIndex(iVal)
            self.assertEqual(iVal, sA.getIndex())
            #
            sVal = "A_STRING_VALUE"
            sA.setName(sVal)
            self.assertEqual(sVal, sA.getName())
            #
            sB = StringA(sVal)
            self.assertEqual(sVal, sB.getName())
            #
            sC = StringA(iVal)
            self.assertEqual(iVal, sC.getIndex())
            #
            sD = StringA(sVal, StringA.eCompareTypeC.eCASE_SENSITIVE)
            self.assertEqual(sVal, sD.getName())
            self.assertEqual(StringA.eCompareTypeC.eCASE_SENSITIVE, sD.getCaseI())

            sE = StringA()
            sE.setCaseG(ptl.eCompareType.eCASE_SENSITIVE)
            self.assertEqual(ptl.eCompareType.eCASE_SENSITIVE, sE.getCaseG())
            #
            sA = StringA()
            s1 = "aa"
            s2 = "bb"
            sVal = "_" + s1 + "." + s2
            tS = sA.methodCombine1(s1, s2)
            self.assertEqual(tS, sVal)
            #
            tS = ""
            tup = sA.methodCombine2(tS, s1, s2)
            # print(tup)
            self.assertEqual(tup, sVal)
            #
            s2L = ["bb1", "bb2", "bb3"]
            tL = []
            rL = ["_" + s1 + "." + s2 for s2 in s2L]
            tup = sA.methodCombine3(tL, s1, s2L)
            self.assertEqual(tup, rL)
            #
            xL = sA.methodSetAndReturn4(s1, s2L)
            self.assertEqual(xL, rL)
            #
            bV = sA.IsEmptyValue("akdsjf")
            self.assertEqual(bV, False)

            bV = sA.IsEmptyValue(".")
            self.assertEqual(bV, True)
            #
            bV = sA.IsEmptyValue("?")
            self.assertEqual(bV, True)
            #
            bV = sA.IsSpecialChar('.')
            self.assertEqual(bV, False)

            bV = sA.IsSpecialChar('[')
            self.assertEqual(bV, True)

        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testSimpleAccessorsB(self):
        """Test case - base class instantiation with ascii data
        """
        try:
            iVal = 100
            sA = StringB()
            sA.setIndex(iVal)
            self.assertEqual(iVal, sA.getIndex())
            #
            sVal = "A_STRING_VALUE"
            sA.setName(sVal)
            self.assertEqual(sVal, sA.getName())
            #
            sB = StringB(sVal)
            self.assertEqual(sVal, sB.getName())
            #
            sC = StringB(iVal)
            self.assertEqual(iVal, sC.getIndex())
            #
            sD = StringB(sVal, StringB.eCompareTypeC.eCASE_SENSITIVE)
            self.assertEqual(sVal, sD.getName())
            self.assertEqual(StringB.eCompareTypeC.eCASE_SENSITIVE, sD.getCaseI())

            sE = StringB()
            sE.setCaseG(ptl.eCompareTypeP.eCASE_SENSITIVE)
            self.assertEqual(ptl.eCompareTypeP.eCASE_SENSITIVE, sE.getCaseG())
            #
            sA = StringB()
            s1 = "aa"
            s2 = "bb"
            sVal = "_" + s1 + "." + s2
            tS = sA.methodCombine1(s1, s2)
            self.assertEqual(tS, sVal)
            #
            tS = ""
            tup = sA.methodCombine2(tS, s1, s2)
            # print(tup)
            self.assertEqual(tup, sVal)
            #
            tS = ""
            tup = sA.methodCombine2(tS, s1, s2, "^", "*")
            # print(tup)
            #
            s2L = ["bb1", "bb2", "bb3"]
            tL = []
            rL = ["_" + s1 + "." + s2 for s2 in s2L]
            tup = sA.methodCombine3(tL, s1, s2L)
            self.assertEqual(tup, rL)
            #
            xL = sA.methodSetAndReturn4(s1, s2L)
            self.assertEqual(xL, rL)
            #
            bV = sA.IsEmptyValue("akdsjf")
            self.assertEqual(bV, False)

            bV = sA.IsEmptyValue(".")
            self.assertEqual(bV, True)
            #
            bV = sA.IsEmptyValue("?")
            self.assertEqual(bV, True)
            #
            bV = sA.IsSpecialChar('.')
            self.assertEqual(bV, False)

            bV = sA.IsSpecialChar('[')
            self.assertEqual(bV, True)

            # Overloaded methods -
            #
            dVal = 1012.345
            sA = StringB()
            sA.setStuff(iVal)
            self.assertEqual(iVal, sA.getIndex())
            sA.setStuff(dVal)
            self.assertEqual(dVal, sA.getDouble())
            #
            kVal = 800
            qVal = 400.234
            #
            sA.setStuff(kVal, qVal)
            self.assertEqual(kVal, sA.getIndex())
            self.assertEqual(qVal, sA.getDouble())
            #
            sA.setStuff(iVal, dVal, StringB.eCompareTypeC.eCASE_SENSITIVE)
            self.assertEqual(iVal, sA.getIndex())
            self.assertEqual(dVal, sA.getDouble())
            self.assertEqual(StringB.eCompareTypeC.eCASE_SENSITIVE, sA.getCaseI())
            #
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testSimpleAccessorsC(self):
        """Test case - base class instantiation with ascii data
        """
        try:
            iVal = 100
            sA = StringC()
            sA.setIndex(iVal)
            self.assertEqual(iVal, sA.getIndex())
            #
            sVal = "A_STRING_VALUE"
            sA.setName(sVal)
            self.assertEqual(sVal, sA.getName())
            #
            sB = StringC(sVal)
            self.assertEqual(sVal, sB.getName())
            #
            sC = StringC(iVal)
            self.assertEqual(iVal, sC.getIndex())
            #
            sD = StringC(sVal, StringC.eCompareTypeC.eCASE_SENSITIVE)
            self.assertEqual(sVal, sD.getName())
            self.assertEqual(StringC.eCompareTypeC.eCASE_SENSITIVE, sD.getCaseI())

            sE = StringC()
            sE.setCaseG(ptl.eCompareTypeG.eCASE_SENSITIVE)
            self.assertEqual(ptl.eCompareTypeG.eCASE_SENSITIVE, sE.getCaseG())
            #
            sA = StringC()
            s1 = "aa"
            s2 = "bb"
            sVal = "_" + s1 + "." + s2
            tS = sA.methodCombine1(s1, s2)
            self.assertEqual(tS, sVal)
            #
            tS = ""
            t = sA.methodCombine2(tS, s1, s2)
            # print(t)
            self.assertEqual(t, sVal)
            #
            tS = ""
            t = sA.methodCombine2(tS, s1, s2, "^", "*")
            # print(t)
            #
            s2L = ["bb1", "bb2", "bb3"]
            tL = []
            rL = ["_" + s1 + "." + s2 for s2 in s2L]
            t = sA.methodCombine3(tL, s1, s2L)
            self.assertEqual(t, rL)
            #
            xL = sA.methodSetAndReturn4(s1, s2L)
            self.assertEqual(xL, rL)
            #
            bV = sA.IsEmptyValue("akdsjf")
            self.assertEqual(bV, False)

            bV = sA.IsEmptyValue(".")
            self.assertEqual(bV, True)
            #
            bV = sA.IsEmptyValue("?")
            self.assertEqual(bV, True)
            #
            bV = sA.IsSpecialChar('.')
            self.assertEqual(bV, False)

            bV = sA.IsSpecialChar('[')
            self.assertEqual(bV, True)

            # Overloaded methods -
            #
            dVal = 1012.345
            sA = StringC()
            sA.setStuff(iVal)
            self.assertEqual(iVal, sA.getIndex())
            sA.setStuff(dVal)
            self.assertEqual(dVal, sA.getDouble())
            #
            kVal = 800
            qVal = 400.234
            #
            sA.setStuff(kVal, qVal)
            self.assertEqual(kVal, sA.getIndex())
            self.assertEqual(qVal, sA.getDouble())
            #
            sA.setStuff(iVal, dVal, StringC.eCompareTypeC.eCASE_SENSITIVE)
            self.assertEqual(iVal, sA.getIndex())
            self.assertEqual(dVal, sA.getDouble())
            self.assertEqual(StringC.eCompareTypeC.eCASE_SENSITIVE, sA.getCaseI())
            #
            #
            #
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    #
    def testSimpleAccessorsFunctions(self):
        """Test case - base class instantiation with ascii data
        """
        try:
            s1 = "aa"
            s2 = "bb"
            sVal = "_" + s1 + "." + s2
            tS = methodCombine1G(s1, s2)
            self.assertEqual(tS, sVal)
            #
            tS = ""
            t = methodCombine2G(tS, s1, s2)
            # print(t)
            self.assertEqual(t, sVal)
            #
            tS = ""
            t = methodCombine2G(tS, s1, s2, "^", "*")
            # print(t)
            #
            s2L = ["bb1", "bb2", "bb3"]
            tL = []
            rL = ["_" + s1 + "." + s2 for s2 in s2L]
            t = methodCombine3G(tL, s1, s2L)
            self.assertEqual(t, rL)
            #
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


def suiteBasic():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(pywraptestlibTests("testSimpleAccessorsA"))
    suiteSelect.addTest(pywraptestlibTests("testSimpleAccessorsB"))
    suiteSelect.addTest(pywraptestlibTests("testSimpleAccessorsC"))
    suiteSelect.addTest(pywraptestlibTests("testSimpleAccessorsFunctions"))
    return suiteSelect


if __name__ == '__main__':
    #
    if (True):
        mySuite = suiteBasic()
        unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)
