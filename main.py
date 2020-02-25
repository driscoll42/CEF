"""
The main file for the project which runs by default validations for all high school and college applicants.
It also generates a score for each applicant based on predefined criteria.
"""

import csv
import re

import constants as cs
from utils import validations as vali, scoring_util as sutil, util


class Student:
    """A student class to track exceptions and values"""


# TODO: Add docstrings
# TODO: Clean up code
# TODO: Implement Sphnix
# TODO: Add DEBUG functionality
# TODO: Add gitignore with emails and passwords, better secure them
# TODO: Package numpy, scipy
# TODO: Extract csv from AwardSpring automatically
# TODO: Replace all csvs with Google Spreadsheets https://www.twilio.tcom/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# TODO: Host this on an AWS server ? https://realpython.com/python-sql-libraries/
# TODO: Make the ACT/SAT/GPA question numeric questions

def compute_HS_scores(file: str):
    """

    Parameters
    ----------
    file

    Returns
    -------

    """
    # Load the conversion factors into a dict to reduce the number of times we have to iterate over the files
    SAT_to_ACT_dict = util.conversion_dict('SAT_to_ACT.csv')
    SAT_to_ACT_Math_dict = util.conversion_dict('SAT_to_ACT_Math.csv')
    school_list = vali.get_school_list('Illinois_Schools.csv')

    # Iterate through file once to get data for histograms
    ACT_Overall, ACTM_Overall = sutil.generate_histo_arrays(file, SAT_to_ACT_dict, SAT_to_ACT_Math_dict)

    '''print('ACT')
    for x in reversed(range(22, 37)):
        print(x, ACT_Overall.count(x), round(percentileofscore(ACT_Overall, x), 2))
    print('ACTM')
    for x in reversed(range(22, 37)):
        print(x, ACTM_Overall.count(x), round(percentileofscore(ACTM_Overall, x), 2))'''

    reviewer_scores = sutil.get_reviewer_scores('Reviewer Scores by Applicant for 2019 Incentive Awards.csv')
    cnt = 0
    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames

        # Check if the questions exist in the file, most often a change in the year
        all_q_exist = True
        for q in cs.questions.values():
            if q not in headers:
                print('ERROR: The following question is not in the headers, check for typos:')
                print(q)
                all_q_exist = False
        if not all_q_exist:
            return

        unique_class = []
        # TODO: Check submission status, if they have not submitted but filled everything out, autowarn?
        for line in d_reader:
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]
            GPA_Value = util.get_num(line[cs.questions['GPA_Value']])
            ACT_SAT_value = util.get_num(line[cs.questions['ACT_SAT_value']])
            ACTM_SATM_value = util.get_num(line[cs.questions['ACTM_SATM_value']])
            COMMS_value = util.get_num(line[cs.questions['COMMS_value']])
            NON_ENG_value = line[cs.questions['NON_ENG_value']]
            student_type = line[cs.questions['student_type']]
            major = line['Major']
            other_major = line[cs.questions['other_major']]
            STEM_Classes = line[cs.questions['STEM_Classes']]
            College = line[cs.questions['College']]
            Other_College = line[cs.questions['Other_College']]
            high_school = line[cs.questions['high_school']]
            high_school_other = line[cs.questions['high_school_other']]

            address1 = line[cs.questions['address1']]
            address2 = line[cs.questions['address2']]
            city = line[cs.questions['city']]
            state = line[cs.questions['state']]
            zip_code = line[cs.questions['zip']]

            # TODO: Overall error handling
            accred_check = ''
            ACT_SAT_Score_check = 0
            # Do below for math too
            '''if ACT_SAT_Score == -1:
                print(ACT_SAT_value, 'No conversion factor exists for this score (is it a decimial?)')
            elif ACT_SAT_Score == -2:
                print(ACT_SAT_value, 'This score is too low for the SAT and too high for the ACT, check if correct')
            elif ACT_SAT_Score == -3:
                print(ACT_SAT_value, 'This score is too high for the SAT, check if correct')'''

            # TODO: Add Distance and time between home and work
            # TODO: Determine school quality
            if 1 == 1 and cs.high_schooler in student_type.upper() and GPA_Value and ACT_SAT_value and ACTM_SATM_value and COMMS_value:
                cnt += 1
                # Check address if residential or commercial
                # Only have 250 free calls per month, commenting this out until needed
                # address_type, home_latitude, home_longitude = vali.address_Validation(lastName, firstName, address1, address2, city, state, zip_code)
                address_type = 'Residential'

                if address_type == 'Invalid Address':
                    print(
                            'WARNING - Applicant has entered an invalid address:  ' + address1 + ' ' + address2 + ' ' + city + ' ' + state + ' ' + zip_code)
                elif address_type != 'Residential':
                    print(
                            'WARNING - Applicant has entered a non-residential address:  ' + address1 + ' ' + address2 + ' ' + city + ' ' + state + ' ' + zip)
                elif address_type == 'Residential' and city.upper() != 'CHICAGO':
                    school = high_school.upper()
                    if high_school == 'My High School is Not Listed':
                        school = high_school_other.upper()
                    if school_list[school] != 'CHICAGO':
                        print('WARNING: Student does neither lives nor goes to high school in Chicago', school)

                # Validation check for Accreditation of college
                College = College.split(',')
                Other_College = Other_College.split(',')
                check = vali.accred_check(College, Other_College, major)
                if not check:
                    accred_check = [College, Other_College, major, other_major]

                # TODO: Coursework functionality
                classes = sutil.class_split(STEM_Classes)
                '''for x in classes:
                    if

                    if x.strip() not in unique_class:
                        unique_class.append(x.strip())'''

                GPA_Score = sutil.GPA_Calc(GPA_Value)
                ACT_SAT_Score = round(sutil.ACT_SAT_Calc(ACT_SAT_value, SAT_to_ACT_dict, 10, ACT_Overall), 2)
                ACTM_SATM_Score = round(sutil.ACT_SAT_Calc(ACTM_SATM_value, SAT_to_ACT_Math_dict, 15, ACTM_Overall), 2)
                COMMS_Score = sutil.COMMS_calc(COMMS_value)
                if major == 'Not listed' and NON_ENG_value:
                    print('Potential non-engineering major, check: ' + NON_ENG_value)

                if lastName.strip().upper() + firstName.strip().upper() in reviewer_scores:
                    reviewer_score = 0.5 * round(reviewer_scores[lastName.strip().upper() + firstName.strip().upper()])
                else:
                    reviewer_score = 0

                print(lastName + ', ' + firstName + ':', GPA_Score, ACT_SAT_Score, ACTM_SATM_Score, COMMS_Score,
                      reviewer_score)
                print(accred_check)

                # TODO: Write back to Excel File or Google Spreadsheets
                # TODO: Send email with new students and warnings
        unique_class.sort()
        print(unique_class)
        print(cnt)


def compute_C_scores(file: str):
    """

    Parameters
    ----------
    file

    Returns
    -------

    """
    recipient_list = vali.get_past_recipients('2019 Recipients.csv')

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames

        all_q_exist = True
        for q in cs.questions.values():
            if q not in headers:
                print('ERROR: The following question is not in the headers, check for typos:')
                print(q)
                all_q_exist = False
        if not all_q_exist:
            return

        for line in d_reader:
            student_type = line[cs.questions['student_type']]
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]
            GPA_Value = line[cs.questions['GPA_Value']]
            major_school_change = line[cs.questions['major_school_change']]
            major = line['Major']
            NON_ENG_value = line[cs.questions['NON_ENG_value']]

            if cs.college_student in student_type.upper():
                if lastName.strip().upper() + firstName.strip().upper() not in recipient_list:
                    # TODO: Implement Fuzzy Name Matching, use for schools and colleges as well
                    print(firstName + ' ' + lastName + ': Student did not receive award last year')

                else:
                    if GPA_Value:
                        GPA_Value = float(GPA_Value)
                        if GPA_Value < 2.75:
                            print(lastName, firstName, 'GPA is below 2.75. GPA is ' + str(GPA_Value))
                        elif GPA_Value < 2.9:
                            print(lastName, firstName, 'GPA is below 2.9, consider warning. GPA is ' + str(GPA_Value))
                    if major_school_change and re.sub('[^A-Za-z0-9]+', '', major_school_change.strip().upper()) != 'NO':
                        print(
                                firstName + ' ' + lastName + ': Major or School Change, investigate: ' + major_school_change)
                    if major == 'Not listed' and NON_ENG_value:
                        print(
                                firstName + ' ' + lastName + ': Other Major Listed, validate it is engineering: ' + NON_ENG_value)


def main():
    """

    """
    filename = 'Student Answers for 2020 Incentive Awards.csv'
    compute_HS_scores(filename)
    compute_C_scores(filename)


main()
