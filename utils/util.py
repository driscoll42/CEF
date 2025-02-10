"""
This file contains various functions which don't classify into scoring or validations and are used throughout the code

get_num - returns first number in a string
conversion_dict - implementation of VLOOKUP for python
name_compare_list - Implements name matching on a string and a list
name_compare - Implements name matching on two strings
"""

import csv
from datetime import datetime, timedelta
from typing import Tuple

import googlemaps
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from classes import Student
from utils import keys as keys


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


def conversion_dict(file_name: str, type: str) -> dict:
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
    with open('dict_Data/' + str(file_name), 'r', encoding="utf-8-sig") as f:
        d_reader = csv.DictReader(f)

        # get fieldnames from DictReader object and store in dict
        headers = d_reader.fieldnames
        header_one = headers[0]
        header_two = headers[1]

        conv_doc = {}

        for line in d_reader:
            if type == 'int':
                conv_doc[int(line[header_one])] = float(line[header_two])
            else:
                conv_doc[line[header_one].upper()] = float(line[header_two])
    return conv_doc


def name_compare_list(name: str, list_of_names: list, minScore: int = 85) -> Tuple[bool, str, int]:
    """Checks for exact match of a string and list, and if not does a fuzzy name match, if no name found it
    returns 'No Close Matching Name'. This is implemented using the fuzzywuzzy package, see link below for details
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

    # First check if the name is in the list of names, typically it is
    if name in list_of_names:
        return True, name, 100

    # If not, then run fuzzy name extract
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
    # Always worthwhile to do a quick exact check first
    if name1 == name2:
        return True, 100

    wratio = fuzz.Wratio(name1, name2)
    if wratio < 85:
        return False, wratio

    return True, wratio


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    new_date = d + timedelta(days_ahead)
    new_date = datetime.strptime(str(new_date), "%Y-%m-%d")
    new_date = new_date.replace(hour=7, minute=00)
    return new_date


def distance_between(s: Student, verbose: bool = False) -> None:
    # Documentation: https://googlemaps.github.io/google-maps-services-python/docs/index.html
    # Source Code and Examples: https://github.com/googlemaps/google-maps-services-python

    gmaps = googlemaps.Client(key=keys.google_api_key)

    # Students probably have to arrive by 7. This forces us to have all students arriving the next Monday
    arrive_time = next_weekday(datetime.now().date(), 0)
    if s.cleaned_address2 is not None:
        home_address = s.cleaned_address1 + ", " + s.cleaned_address2 + ", " + s.cleaned_city + ", " + s.cleaned_state + ", " + s.cleaned_zip_code
    else:
        home_address = s.cleaned_address1 + ", " + s.cleaned_city + ", " + s.cleaned_state + ", " + s.cleaned_zip_code

    # TODO: Get the real school address instead of just the school name
    if s.high_school_full != 'Homeschooled':
        try:
            directions_result = gmaps.directions(home_address,
                                                 s.high_school_full,
                                                 mode="driving",  # mode="transit"
                                                 arrival_time=arrive_time,
                                                 # traffic_model='best_guess',
                                                 region="us")

            s.home_to_school_dist = float(directions_result[0]['legs'][0]['distance']['text'].split()[0])
            # TODO: Duration outputs like 1 hour 9 mins, make this like 1:09
            s.home_to_school_time_car = directions_result[0]['legs'][0]['duration']['text']
            split_string = s.home_to_school_time_car.split()
            for string, i in enumerate(split_string):
                num_store = 0
                if i % 2 == 0:
                    num_store = int(string)
                else:
                    pass

        except Exception as e:
            print('Error getting Driving Directions for')
            print(home_address, s.high_school_full)
            print(e)

        try:
            directions_result = gmaps.directions(home_address,
                                                 s.high_school_full,
                                                 mode="transit",
                                                 arrival_time=arrive_time,
                                                 # traffic_model='best_guess',
                                                 region="us")
            s.home_to_school_time_pt = directions_result[0]['legs'][0]['duration']['text']
        except Exception as e:
            print('Error getting Transit Directions for')
            print('Home Address', home_address)
            print('School Address', s.high_school_full)
            print(e)
    else:
        s.home_to_school_dist = 'Homeschooled'
        s.home_to_school_time_car = 'Homeschooled'
        s.home_to_school_time_pt = 'Homeschooled'

        # The maximum distance a student should travel is to IMSA from Chicago, which at the most is 64 miles, rounding
    #   up to 70 to accomodate oddities
    # Most likely this means the code is finding the wrong high school to compute distances, there are many "Washington
    #   High School"s in the USA
    if s.home_to_school_dist > 70:
        s.distance_warn = False
        s.validationError = True
        if verbose:
            print('WARNING: Student lives an unusually far distance away: ', s.home_to_school_dist, 'miles')
            print('Home Address', home_address)
            print('School Address', s.high_school_full)


def get_review_feedback(file_name):
    reviewer_df = pd.read_excel(f'Student_Data/{file_name}')
    agg_rev_df = reviewer_df.fillna('').groupby(['Applicant']).agg({'Community Service / Work'  : ['mean'],
                                                                    'Short Essay'               : ['mean'],
                                                                    'Bonus/Discretionary Points': ['mean'],
                                                                    'Notes'                     : [
                                                                        ' || '.join]}).reset_index()
    agg_rev_df.columns = ['_'.join(col) for col in agg_rev_df.columns]

    return agg_rev_df
