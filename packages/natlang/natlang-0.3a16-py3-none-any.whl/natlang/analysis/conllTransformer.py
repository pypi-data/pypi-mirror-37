# -*- coding: utf-8 -*-
# Python version: 2/3
#
# This script transforms a dependency tree loaded with natlang.format.conll
# Simon Fraser University
# Jetic Gu
#
from __future__ import print_function
from __future__ import absolute_import

import os
import sys
import copy
import inspect
import unittest
import progressbar

from natlang.loader import DataLoader
from natlang.format import conll


# Patter specification
# The pattern is a string with tree structure
# Here are some examples
#
#   ( (* nsubj *) | root | (* advmod *) )
#   This matches any tree with a subtree, the root of which has a nsubj as
#   leftChild and an advmod as right child
#
def parseBrackets(pattern):
    result = []
    counter = 0
    pattern = pattern.replace('(', " ( ").replace(')', " ) ")
    pattern = pattern.strip().split()
    if pattern[0] != '(':
        pattern = ['('] + pattern
        pattern = [')'] + pattern
    return closeBrackets(pattern)


def closeBrackets(pattern, startIndex=0):
    entry = []
    counter = 0
    i = startIndex
    while i < len(pattern):
        if pattern[i] == '(':
            counter += 1
            if counter > 1:
                subEntry, i = closeBrackets(pattern, i)
                entry.append(subEntry)
                continue
        elif pattern[i] == ')':
            counter -= 1
            if counter < 0:
                raise ValueError(
                    "natlang.analysis.conllTransformer.closeBrackets: " +
                    "invalid pattern, brackets not closed")
            if counter == 0:
                return entry, i
        else:
            entry.append(pattern[i])
        i += 1
    if counter != 0:
        raise ValueError(
            "natlang.analysis.conllTransformer.closeBrackets: invalid " +
            "pattern, brackets not closed")
    return entry, i


def matchPattern(pattern, node):
    candidates = []

    # Value check
    if not isinstance(pattern, str):
        raise ValueError(
            "natlang.analysis.conllTransformer.matchPattern: pattern must " +
            "be a str")

    if not isinstance(node, conll.Node):
        raise ValueError(
            "natlang.analysis.conllTransformer.node: pattern must be a" +
            "natlang.format.conll.Node instance ")

    # bracket parser
    def parseBrackets(pattern):
        result = []
        counter = 0
        pattern.replace('(', " ( ").replace(')', " ) ")
        pattern = pattern.strip().split()
        return

    return candidates


class TestTree(unittest.TestCase):
    def testParseBracket1(self):
        content, _ = parseBrackets("(closeBrackets(pattern))")
        answer = ["closeBrackets", ["pattern"]]
        self.assertSequenceEqual(content, answer)
        return


if __name__ == '__main__':
    if not bool(getattr(sys, 'ps1', sys.flags.interactive)):
        unittest.main()
