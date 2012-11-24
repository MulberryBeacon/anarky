#!/usr/bin/python -tt

# Module import section
# -------------------------------------------------------------------------------------------------
from itertools import tee, islice, chain, izip


# Constants :: Text formatting
# -------------------------------------------------------------------------------------------------
TAB = "    "


# Methods :: Text manipulation
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Checks if a string is empty.
#
# @param string Text sequence to check
# @return True if the given string is empty; false otherwise
# *************************************************************************************************
def is_string_empty(string):
	return string is None or len(string) == 0


# *************************************************************************************************
# Inserts the equivalent of a tab in a string (incremental implementation).
#
# @param number Number of tabs
# @return The concatenation of 'number' occurrences of the tab string
# *************************************************************************************************
def indent_inc(number):
	if (number <= 0):
		return ""

	text = ""
	for i in range(0, number):
		text += TAB

	return text


# *************************************************************************************************
# Inserts the equivalent of a tab in a string (recursive implementation).
#
# @param number Number of tabs
# @return The concatenation of 'number' occurrences of the tab string
# *************************************************************************************************
def indent(number):
	if (number <= 0):
		return ""

	if (number == 1):
		return TAB

	return TAB + indent(number - 1)


# Methods :: List manipulation
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Goes through a list of tuples and pairs them.
# As an example, consider the following list of tuples:
# [(A1,A2), (B1,B2), (C1,C2)]
#
# The resulting list of pairs will be:
# [((A1,A2), (B1,B2)), ((B1,B2), (C1,C2)), ((C1,C2), None)]
#
# @param tuple_list List of tuples
# @return A list of pairs of tuples
# *************************************************************************************************
def get_tuple_pairs(tuple_list):
	current, next = tee(tuple_list, 2)
	next = chain(islice(next, 1, None), [None])
	return izip(current, next)
