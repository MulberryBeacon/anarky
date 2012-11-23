#!/usr/bin/python -tt

# Methods :: Text manipulation
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Checks if a string is empty.
#
# @param string Text sequence to check
# @return True if the given string is empty; false otherwise
# *************************************************************************************************
def isstringempty(string):
	return string is None or len(string) == 0


# *************************************************************************************************
# Inserts the equivalent of a tab in a string (incremental implementation).
#
# @param number Number of tabs
# @return The concatenation of 'number' occurrences of the tab string
# *************************************************************************************************
def indent(tab, number):
	if (number <= 0):
		return ""

	text = ""
	for i in range(0, number):
		text += tab

	return text


# *************************************************************************************************
# Inserts the equivalent of a tab in a string (recursive implementation).
#
# @param number Number of tabs
# @return The concatenation of 'number' occurrences of the tab string
# *************************************************************************************************
def indent_rec(tab, number):
	if (number <= 0):
		return ""

	if (number == 1):
		return tab

	return tab + indent_rec(number - 1)
