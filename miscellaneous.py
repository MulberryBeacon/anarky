#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Set of miscellaneous functions.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import section
# -------------------------------------------------------------------------------------------------
from itertools import tee, islice, chain, izip

# Constants :: Text formatting
# -------------------------------------------------------------------------------------------------
TAB = "    "


# Methods :: Text manipulation
# -------------------------------------------------------------------------------------------------
def is_string_empty(string):
	"""
	Checks if a string is empty.
	"""
	return string is None or len(string) == 0


def indent(number):
	"""
	Inserts 'number' occurrences of the equivalent of a tab in a string (incremental implementation).
	"""
	if (number <= 0):
		return ""

	text = ""
	for i in range(0, number):
		text += TAB

	return text


def tab(number):
	"""
	Inserts 'number' occurrences of the equivalent of a tab in a string (recursive implementation).
	"""
	if (number <= 0):
		return ""

	if (number == 1):
		return TAB

	return TAB + tab(number - 1)


# Methods :: List manipulation
# -------------------------------------------------------------------------------------------------
def get_tuple_pairs(tuple_list):
	"""
	Goes through a list of tuples and pairs them. For instance, consider the list of tuples:
	[(A1,A2), (B1,B2), (C1,C2)]

	The resulting list of pairs will be:
	[((A1,A2), (B1,B2)), ((B1,B2), (C1,C2)), ((C1,C2), None)]
	"""
	current, next = tee(tuple_list, 2)
	next = chain(islice(next, 1, None), [None])
	return izip(current, next)
