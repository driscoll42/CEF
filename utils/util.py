"""
This file contains various functions which don't classify into scoring or validations and are used throughout the code

get_num - returns first number in a string
conversion_dict - implementation of VLOOKUP for python
name_compare_list - Implements fuzzy name matching on a string and a list
name_compare - Implements fuzzy name matching on two strings
"""

import csv
from typing import Tuple

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# Too much of the data is dirty often times, this function gets the first number in a string, and returns it
# If there is no number, or it's NULL, it returns a 0
def get_num(input_text: str) -> float:
    """Returns the first number in a string.

    Parameters
    ----------
    input_text : str
        The input_text that should (but does not need) contain at least one number

    Returns
    -------
    object : float
        The first number in the input_text, or a 0.0 if no number found
    """

    # https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python/4289415#4289415
    list_of_nums = []
    for t in input_text.split():
        try:
            list_of_nums.append(float(t))
        except ValueError:
            pass

    if len(list_of_nums) == 0:
        return 0.0
    else:
        return float(list_of_nums[0])


def conversion_dict(file_name: str) -> dict:
    """This is basically VLOOKUP from Excel, for an input file it creates a dictionary where the first column is the
    key and the second column is the value. Currently assumes all values are integers

    Parameters
    ----------
    file_name : str
        A csv file containing what conversions are to be created, assumes all values are integers

    Returns
    -------
    conv_doc : dict
        A dictionary where the key is the value you need converted and the value is the desired output

    """
    # This function assumes your from value is in the first column of the csv and your to is in the second
    # Further it assumes the first column has not repeats
    # Also assumes that all the values in the table are integers
    with open('Conversions/' + str(file_name), 'r', encoding="utf-8-sig") as f:
        d_reader = csv.DictReader(f)

        # get fieldnames from DictReader object and store in dict
        headers = d_reader.fieldnames
        header_one = headers[0]
        header_two = headers[1]

        conv_doc = {}

        for line in d_reader:
            conv_doc[int(line[header_one])] = int(line[header_two])

    return conv_doc


def name_compare_list(name: str, list_of_names: list, minScore: int = 85) -> Tuple[bool, str, int]:
    """Implements fuzzy name matching on a string and a list, if no name found it returns 'No Close Matching Name'
    This is implemented using the fuzzywuzzy package, see link below for details
    https://www.datacamp.com/community/tutorials/fuzzy-string-python

    Parameters
    ----------
    name : str
        The name trying to find if exists in list
    list_of_names : str
        A list of known good names

    Returns
    -------
    cleaned_name : str
        The name from the list which most closely matches name. Or if the score is below 85, no name
    cleaned_name : str
        The name from the list which most closely matches name. Or if the score is below 85, no name
    wratio : str
        The name from the list which most closely matches name. Or if the score is below 85, no name
    """

    cleaned_name = process.extractOne(name, list_of_names)
    if cleaned_name[1] < minScore:
        return False, 'No Close Matching Name', cleaned_name[1]

    return True, cleaned_name[0], cleaned_name[1]


def name_compare(name1: str, name2: str) -> Tuple[bool, int]:
    """Implements fuzzy name matching on two strings, returns True if close, False if not
    This is implemented using the fuzzywuzzy package, see link below for details
    https://www.datacamp.com/community/tutorials/fuzzy-string-python

    Parameters
    ----------
    name : str
        The first name to compare
    list_of_names : str
        The second name to compare

    Returns
    -------
    cleaned_name : str
        A bool if the two names are similar enough
    wratio : int
        The wratio of the two numbers
    """

    wratio = fuzz.Wratio(name1, name2)
    if wratio < 85:
        return False, wratio

    return True, wratio
