"""
This file contains a number of validations to confirm that an applicant is qualified for an award.

High School Students:
address_validation - Validates if an applicant's address is a real residence, if they live or go to school in in Chicago
resident_validation - Verify applicant lives in Chicago
accred_check - Verify applicant is accepted into an ABET accredited program
school_name_reduce - Removes common words from school name

College students:
past_recipient - Validates if a college student is a past recipient of the award
college_gpa - Checks if a past recipients GPA meets the threshold
college_school_major - Validates if a college student has changed their major or school
get_past_recipients - get a list of past recipients to verify they recieved it as a high school senior
get_school_list - returns list of Illinois high schools

Misc.:
questions_check - Checks if all questions in the constants file exist in the csv header
list_failures - TBD
"""

import csv
import re
from typing import Tuple

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

import constants as cs
from classes import Student
from utils import keys as keys
from utils import util


def address_validation(s: Student, chicago_schools: list, school_list: dict, verbose: bool = False, DEBUG: bool = False,
                       CALL_APIS: bool = False) -> None:
    """Validates if an applicant's address is a real residence, if they live or go to school in in Chicago

    Parameters
    ----------
    s : Student
        A member of the Student class
    chicago_schools : list
        A list of all Chicago high schools
    school_list : list
        A list of all Illinois high schools

    Returns
    -------
    """
    # Check address if residential or commercial and get cleaned up address
    if CALL_APIS:
        resident_validation(s, verbose, DEBUG)

    s.address_type = 'Residential'

    if s.address_type == 'Residential' and s.city.upper() != 'CHICAGO':
        if s.high_school_full.upper().strip() not in chicago_schools:
            s.high_school_partial = school_name_reduce(s.high_school_full, s.high_school_other)
            # This is an computationally EXPENSIVE operation, avoid as much as possible
            school_bool, school, school_score = util.name_compare_list(s.high_school_partial,
                                                                       school_list.keys(), 95)
            if school_bool:
                s.high_school_full = school
                # print(s.high_school_full, ' - ', school, school_score, school_list[school], s.city)
                # Trial and error has found 95 to be required to ONLY get correct matches, 90 works the vast majoriy, but some false positives get through
                if school_list[school].upper() != 'CHICAGO':
                    # print(orig_School, ' - ', school, school_score, school_list[school], s.city)
                    s.ChicagoSchool = False
                    if verbose:
                        print('WARNING: Student does neither lives nor goes to high school in Chicago', school)
            else:
                s.school_found = False
                if verbose:
                    print('Could not find matching school in system')
                    print(s.high_school_full, ' - ', school, school_score, s.city)

    if CALL_APIS:
        util.distance_between(s)


# Source: https://smartystreets.com/docs/sdk/python
def resident_validation(s: Student, verbose: bool = False, DEBUG: bool = False) -> None:
    """This function will check a given address to determine what type of address it is, either residential, commercial,
        or if it is invalid. If the address is valid, it will also return the longitude and latitude of the address

    Parameters
    ----------
    lastName : str
        Applicant's last name
    firstName : str
        Applicant's first name
    address1 : str
        Applicant's home address line 1
    address2 : str
        Applicant's home address line 2
    city : str
        Applicant's home city
    state : str
        Applicant's home state
    zip_code : str
        Applicant's home zip_code

    Returns
    -------
    residency : str
        'Residential', 'Commercial', or 'Invalid Address' based on the USPS database
    latitude : float
        The latitude of the address given
    longitude : float
        The longitude of the address given

    """
    # We recommend storing your secret keys in environment variables instead---it's safer!
    # auth_id = os.environ['SMARTY_AUTH_ID']
    # auth_token = os.environ['SMARTY_AUTH_TOKEN']

    credentials = StaticCredentials(keys.auth_id, keys.auth_token)

    client = ClientBuilder(credentials).build_us_street_api_client()
    # client = ClientBuilder(credentials).with_custom_header({'User-Agent': 'smartystreets (python@0.0.0)', 'Content-Type': 'application/json'}).build_us_street_api_client()
    # client = ClientBuilder(credentials).with_proxy('localhost:8080', 'user', 'password').build_us_street_api_client()
    # Uncomment the line above to try it with a proxy instead

    # Documentation for input fields can be found at:
    # https://smartystreets.com/docs/us-street-api#input-fields

    lookup = StreetLookup()
    lookup.input_id = ""  # Optional ID from your system
    lookup.addressee = s.firstName + " " + s.lastName
    lookup.street = s.address1
    lookup.street2 = ""
    lookup.secondary = s.address2
    lookup.urbanization = ""  # Only applies to Puerto Rico addresses
    lookup.city = s.city
    lookup.state = s.state
    lookup.zipcode = s.zip_code
    lookup.candidates = 3
    lookup.match = "strict"  # "invalid" is the most permissive match,
    # this will always return at least one result even if the address is invalid.
    # Refer to the documentation for additional Match Strategy options.
    # This has been modified to strict to only get valid addresses

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        s.other_error = False
        s.other_error_message = s.other_error_message + ' - resident_validation failed with error: ' + err

    result = lookup.result

    if not result:
        if verbose:
            print("No candidates. This means the address is not valid.")
        s.valid_address = False
    else:
        first_candidate = result[0]
        s.address_type = first_candidate.metadata.rdi
        s.home_latitude = first_candidate.metadata.latitude
        s.home_longitude = first_candidate.metadata.longitude
        s.cleaned_address1 = first_candidate.delivery_line_1
        s.cleaned_address2 = first_candidate.delivery_line_2
        s.cleaned_city = first_candidate.components.city_name
        s.cleaned_state = first_candidate.components.state_abbreviation
        s.cleaned_zip_code = first_candidate.components.zipcode
        s.address_footnotes = first_candidate.analysis.footnotes


def past_recipient(s: Student, list_of_students: list, verbose: bool = False, DEBUG: bool = False) -> bool:
    """Validates if a college student is a past recipient of the award

    Parameters
    ----------
    s : Student
        A member of the Student class
    list_of_students : list
        A list of all past recipients of the award

    Returns
    -------
    compare_test : bool
        True or False if the student is a past recipient or not
    """
    student_name = s.firstName + ' ' + s.lastName
    compare_test, name, wratio = util.name_compare_list(student_name, list_of_students)
    if not compare_test:
        s.past_recipient = False
        s.validationError = True
        if verbose:
            print(s.firstName + ' ' + s.lastName + ': Student did not receive award last year')
    return compare_test


def college_gpa(s: Student, verbose: bool = False, DEBUG: bool = False) -> None:
    """Checks if a past recipients GPA meets the threshold

    Parameters
    ----------
    s : Student
        A member of the Student class

    Returns
    -------
    """
    if s.GPA_Value:
        s.GPA_Value = float(s.GPA_Value)

        if s.GPA_Value < cs.minimum_gpa:
            s.GPA_C_Under = False
            s.validationError = True
            if verbose:
                print(s.lastName, s.firstName, 'GPA is below 2.75. GPA is ' + str(s.GPA_Value))
        elif s.GPA_Value < cs.warning_gpa:
            s.GPA_C_Warn = False
            s.validationError = True
            if verbose:
                print(s.lastName, s.firstName, 'GPA is below 2.9, consider warning. GPA is ' + str(s.GPA_Value))


def college_school_major(s: Student, verbose: bool = False, DEBUG: bool = False) -> None:
    """Validates if a college student has changed their major or school

    Parameters
    ----------
    s : Student
        A member of the Student class

    Returns
    -------
    """
    # TODO: Check that their major is still engineering even if they don't say they changed
    if s.major_school_change and re.sub('[^A-Za-z0-9]+', '', s.major_school_change.strip().upper()) not in ['NO', 'NA']:
        s.C_College_change = False
        s.validationError = True
        if verbose:
            print(s.firstName + ' ' + s.lastName + ': Major or School Change, investigate: ' + s.major_school_change)
    if s.major == 'Not listed' and s.NON_ENG_value:
        s.C_Major_Warn = False
        s.validationError = True
        if verbose:
            print(
                s.firstName + ' ' + s.lastName + ': Other Major Listed, validate it is engineering: ' + s.NON_ENG_value)


def accred_check(s: Student, verbose: bool = False, DEBUG: bool = False) -> None:
    """This function will determine if the applicant is going to an ABET accredited program. This requires that an
    extract from ABET's website in the "School_Data" folder. As an applicant can have multiple schools listed, this
    function iterates over all of them and checks if they are in the ABET list. If so it then compares the major the
    applicant is taking and sees if the program is accredited at that school. If the applicant's major is "Undecided
    Engineering", the function just checks that the school has ABET accredited engineering programs.


    Parameters
    ----------
    school_list : list
        The list of all the school's the applicant is accepted to from a predefined list setup on AwardSpring
    other_school : list
        The list of schools the applicant is accepted to from the free form field if the above is "Not Listed"
    major : str
        A string containing the majors the applicatn is applying for

    Returns
    -------
    accredited : bool
        A bool if the school and major combination is accredited or not

    """
    # TODO: Implement Fuzzy Name for school and major matching
    school_list = s.College.split(',')
    other_school_list = s.Other_College.split(',')

    major = s.major.upper()
    major = major.strip()
    major = major.replace(' AND ', ',')
    major = major.replace(' ', '')
    major = major.replace('ENGINEERING', '')
    major_list = major.split(',')

    for school in school_list:
        school = school.upper()
        school = school.strip()
        school = school.replace('THE ', '')
        school = school.replace(' AT ', ' - ')
        school = school.replace('-', '')
        school = school.replace(' ', '')

        with open('School_Data/ABET_Accredited_Schools.csv', 'r', encoding="utf-8-sig") as f:
            d_reader = csv.DictReader(f)
            for line in d_reader:
                ABET_major = line[cs.abet_major]
                ABET_major = ABET_major.upper()
                ABET_major = ABET_major.strip()
                ABET_major = ABET_major.replace(' AND ', ',')
                ABET_major = ABET_major.replace(' ', '')
                ABET_major = ABET_major.replace('ENGINEERING', '')

                ABET_school = line[cs.abet_school_name]
                ABET_school = ABET_school.upper()
                ABET_school = ABET_school.strip()
                ABET_school = ABET_school.replace('THE ', '')
                ABET_school = ABET_school.replace(' AT ', ' - ')
                ABET_school = ABET_school.replace('-', '')
                ABET_school = ABET_school.replace(' ', '')
                if school in ABET_school:
                    for option in major_list:
                        if option == ABET_major or option == 'UNDECIDED' or option == '':
                            return

    for school in other_school_list:
        school = school.upper()
        school = school.strip()
        school = school.replace('THE ', '')
        school = school.replace(' AT ', ' - ')
        school = school.replace('-', '')
        school = school.replace(' ', '')

        with open('School_Data/ABET_Accredited_Schools.csv', 'r', encoding="utf-8-sig") as f:
            d_reader = csv.DictReader(f)
            for line in d_reader:
                ABET_major = line[cs.abet_major]
                ABET_major = ABET_major.upper()
                ABET_major = ABET_major.strip()
                ABET_major = ABET_major.replace(' AND ', ',')
                ABET_major = ABET_major.replace(' ', '')
                ABET_major = ABET_major.replace('ENGINEERING', '')

                ABET_school = line[cs.abet_school_name]
                ABET_school = ABET_school.upper()
                ABET_school = ABET_school.strip()
                ABET_school = ABET_school.replace('THE ', '')
                ABET_school = ABET_school.replace(' AT ', ' - ')
                ABET_school = ABET_school.replace('-', '')
                ABET_school = ABET_school.replace(' ', '')
                if school in ABET_school:
                    for option in major_list:
                        if option == ABET_major or option == 'UNDECIDED' or option == '':
                            return

    s.accredited = False

    if s.major == 'Not Listed':
        s.valid_major = False  # TODO: This probably needs work
        if verbose:
            print('Potential non-engineering major, check: ' + s.NON_ENG_value)


def get_past_recipients(file: str, verbose: bool = False, DEBUG: bool = False) -> list:
    """ A simple function to turn a file containing the list of past recipients of the award into a list

    Parameters
    ----------
    file : str
        A csv containing a list of past recipients

    Returns
    -------
    recipient_list: list
        A list with all the names of the past recipients
    """
    recipient_list = []

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]
            recipient_list.append(firstName.strip() + ' ' + lastName.strip())
    return recipient_list


def get_school_list(file: str, verbose: bool = False, DEBUG: bool = False) -> Tuple[dict, list]:
    """ A simple function to turn a file containing the list of high schools in Illinois with their city and return it
        as a dict. Also it returns a list of all Chicago high schools (to reduce fuzzy calls)

    Parameters
    ----------
    file : str
        A csv containing a list of high school/city combinations

    Returns
    -------
    school_list: dict
        A dictionary with a key of high school name and a value of the city the school is in
    chicago_schools: dict
        A list of all Chicago high schools
    """
    school_list = {}
    chicago_schools = []
    with open('School_Data/' + str(file), 'r') as f:
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames
        # print(headers)
        for line in d_reader:
            # Far too many of the schools have the word school and others in them which makes a fuzzy match score too high
            orig_school_name = line['FacilityName']
            school_name = school_name_reduce(orig_school_name, '')

            school_list[school_name] = line['City']
            if line['City'].upper() == 'CHICAGO':
                chicago_schools.append(orig_school_name.upper().strip())

    return school_list, chicago_schools


def questions_check(question_list: list, verbose: bool = False, DEBUG: bool = False) -> bool:
    """Checks if all questions in the constants file exist in the csv header

    Parameters
    ----------
    question_list : list
        A list of all the questions in the csv header

    Returns
    -------
    all_q_exist : bool
        A true or false if all questions exist in the csv header

    """
    all_q_exist = True
    for q in cs.questions.values():
        if q not in question_list:
            print('ERROR: The following question is not in the headers, check for typos: ' + str(q))
            all_q_exist = False
            break

    return all_q_exist


def school_name_reduce(school_name: str, other_school: str, verbose: bool = False, DEBUG: bool = False) -> str:
    """For the fuzzy name logic, it's easier if the common text is removed from a school name. For example too many
    have "High School" in the name leading to higher fuzzy scores.

    Parameters
    ----------
    school_name : str
        The school name in from predefined list
    other_school : str
        A school name from a freeform school field

    Returns
    -------
    school_name : str
        The reduced school_name

    """
    # TODO: If a student lists multiple high schools?
    # TODO: How to deal with the same school name in multiple cities?
    # TODO: Issue such as Trinity Academy and Trinity High School

    if school_name == 'My High School is Not Listed':
        school_name = other_school

    school_name = school_name.replace(' High School', '')
    school_name = school_name.replace(' Middle School', '')
    school_name = school_name.replace(' Elementary School', '')
    school_name = school_name.replace(' College Prep', '')
    school_name = school_name.replace(' Academy', '')
    school_name = school_name.replace(' School', '')
    return school_name


def list_failures(student_list: list, student_type: str, verbose: bool = False, DEBUG: bool = False):
    """

    Parameters
    ----------
    student_list : list
        A list containing all the students as the student class
    student_type : str
        If the student is a high school or college student

    Returns
    -------

    """
    for s in student_list:
        if s.address_type == 'Invalid Address':
            print(
                    'WARNING - Applicant has entered an invalid address:  ' + s.address1 + ' ' + s.address2 + ' ' + s.city + ' ' + s.state + ' ' + s.zip_code)
        elif s.address_type != 'Residential':
            print(
                    'WARNING - Applicant has entered a non-residential address:  ' + s.ddress1 + ' ' + s.address2 + ' ' + s.city + ' ' + s.state + ' ' + s.zip_code)


'''if ACT_SAT_Score == -1:
    print(ACT_SAT_value, 'No conversion factor exists for this score (is it a decimial?)')
elif ACT_SAT_Score == -2:
    print(ACT_SAT_value, 'This score is too low for the SAT and too high for the ACT, check if correct')
elif ACT_SAT_Score == -3:
    print(ACT_SAT_value, 'This score is too high for the SAT, check if correct')'''
