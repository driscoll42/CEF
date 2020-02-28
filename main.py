"""
The main file for the project which runs by default validations for all high school and college applicants.
It also generates a score for each applicant based on predefined criteria.
"""

import csv
import re

import constants as cs
from classes import Student
from utils import validations as vali, scoring_util as sutil, util


# TODO: Clean up code
# TODO: Implement Sphnix
# TODO: Add DEBUG functionality
# TODO: Add gitignore with emails and passwords, better secure them
# TODO: Package numpy, scipy
# TODO: Extract csv from AwardSpring automatically - https://automatetheboringstuff.com/2e/chapter12/
# TODO: Replace all csvs with Google Spreadsheets https://www.twilio.tcom/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html https://automatetheboringstuff.com/2e/chapter14/
# TODO: Host this on an AWS server ? https://realpython.com/python-sql-libraries/


def compute_HS_scores(file: str):
    """The main function that computes the high school student's scores and validates their application

    Parameters
    ----------
    file : str
        The file with all of the student's answers

    Returns
    -------

    """
    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames

        # Check if the questions exist in the file, most often a change in the year
        if not vali.questions_check(headers):
            return

        # Load the conversions and lists into variables for reuse
        SAT_to_ACT_dict = util.conversion_dict('SAT_to_ACT.csv')
        SAT_to_ACT_Math_dict = util.conversion_dict('SAT_to_ACT_Math.csv')
        school_list, chicago_schools = vali.get_school_list('Illinois_Schools.csv')

        # Iterate through file once to get data for histograms
        ACT_Overall, ACTM_Overall = sutil.generate_histo_arrays(file, SAT_to_ACT_dict, SAT_to_ACT_Math_dict)

        reviewer_scores = sutil.get_reviewer_scores('Reviewer Scores by Applicant for 2019 Incentive Awards.csv')
        unique_class = []
        student_list = []
        # TODO: Check submission status, if they have not submitted but filled everything out, autowarn?

        for line in d_reader:
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]

            s = Student.Student(firstName, lastName)

            s.GPA_Value = util.get_num(line[cs.questions['GPA_Value']])
            s.ACT_SAT_value = util.get_num(line[cs.questions['ACT_SAT_value']])
            s.ACTM_SATM_value = util.get_num(line[cs.questions['ACTM_SATM_value']])

            s.COMMS_value = util.get_num(line[cs.questions['COMMS_value']])
            s.NON_ENG_value = line[cs.questions['NON_ENG_value']]
            s.student_type = line[cs.questions['student_type']]

            s.major = line['Major']
            s.other_major = line[cs.questions['other_major']]
            s.STEM_Classes = line[cs.questions['STEM_Classes']]

            s.College = line[cs.questions['College']]
            s.Other_College = line[cs.questions['Other_College']]
            s.high_school_full = line[cs.questions['high_school']]
            s.high_school_other = line[cs.questions['high_school_other']]

            s.address1 = line[cs.questions['address1']]
            s.address2 = line[cs.questions['address2']]
            s.city = line[cs.questions['city']]
            s.state = line[cs.questions['state']]
            s.zip_code = line[cs.questions['zip']]

            # TODO: Overall error handling
            # TODO: Add Distance and time between home and work
            # TODO: Determine school quality

            # A basic saity check that if the GPA and ACT values are populated, then the applicant is probably applying
            # TODO: Add essay length
            if 1 == 1 and cs.high_schooler in s.student_type.upper() and s.GPA_Value and s.ACT_SAT_value and s.ACTM_SATM_value and s.COMMS_value:
                # Validate the applicant's address is residential and that they live or go to high school in Chicago

                # Check address if residential or commercial
                # Only have 250 free calls per month, commenting this out until needed
                # s.address_type, s.home_latitude, s.home_longitude = vali.address_Validation(lastName, firstName, address1, address2, city, state, zip_code)
                s.address_type = 'Residential'

                if s.address_type == 'Residential' and s.city.upper() != 'CHICAGO':
                    s.high_school_partial = vali.school_name_reduce(s.high_school_full, s.high_school_other)

                    if s.high_school_full.upper().strip() not in chicago_schools:
                        # This is an EXPENSIVE operation, avoid as much as possible
                        school_bool, school, school_score = util.name_compare_list(s.high_school_partial,
                                                                                   school_list.keys(), 95)
                        if school_bool:
                            s.high_school_full = school
                            # print(s.high_school_full, ' - ', school, school_score, school_list[school], s.city)
                            # Trial and error has found 95 to be required to ONLY get correct matches, 90 works the vast majoriy, but some false positives get through
                            if school_list[school].upper() != 'CHICAGO':
                                # print(orig_School, ' - ', school, school_score, school_list[school], s.city)
                                print('WARNING: Student does neither lives nor goes to high school in Chicago', school)
                        else:
                            print('Could not find matching school in system')
                            print(s.high_school_full, ' - ', school, school_score, s.city)

                # Validate the applicant is accepted into an ABET engineering program
                s.College = s.College.split(',')
                s.Other_College = s.Other_College.split(',')
                check = vali.accred_check(s.College, s.Other_College, s.major)  # TODO: Implement Fuzzy Name
                if not check:
                    accred_check = [s.College, s.Other_College, s.major, s.other_major]
                if s.major == 'Not listed' and s.NON_ENG_value:
                    print('Potential non-engineering major, check: ' + s.NON_ENG_value)

                # Validate the applicants ACT/SAT scores and score their GPA and ACT/SAT
                sutil.GPA_Calc(s)
                sutil.ACT_SAT_Calc(s, SAT_to_ACT_dict, ACT_Overall, 'C')
                sutil.ACT_SAT_Calc(s, SAT_to_ACT_Math_dict, ACTM_Overall, 'M')

                # TODO: Coursework functionality
                # Score the applicant's coursework
                classes = sutil.class_split(s.STEM_Classes)
                '''for x in classes:
                    if

                    if x.strip() not in unique_class:
                        unique_class.append(x.strip())'''

                if lastName.strip().upper() + firstName.strip().upper() in reviewer_scores:
                    reviewer_score = 0.5 * round(reviewer_scores[lastName.strip().upper() + firstName.strip().upper()])
                else:
                    reviewer_score = 0

                # print(lastName + ', ' + firstName + ':', GPA_Score, ACT_SAT_Score, ACTM_SATM_Score, reviewer_score)
                # print(accred_check)

                # TODO: Write back to Excel File or Google Spreadsheets
                # TODO: Send email with new students and warnings https://automatetheboringstuff.com/2e/chapter18/
            student_list.append(s)

        unique_class.sort()


def compute_C_scores(file: str):
    """The main function that checks college student's eligibility for the award

    Parameters
    ----------
    file : str
        The file with all of the student's answers


    Returns
    -------

    """

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames

        # Check if the questions exist in the file, most often a change in the year
        if not vali.questions_check(headers):
            return

        recipient_list = vali.get_past_recipients('2019 Recipients.csv')

        for line in d_reader:
            student_type = line[cs.questions['student_type']]
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]
            GPA_Value = line[cs.questions['GPA_Value']]
            major_school_change = line[cs.questions['major_school_change']]
            major = line['Major']
            NON_ENG_value = line[cs.questions['NON_ENG_value']]

            if cs.college_student in student_type.upper():
                student_name = firstName + ' ' + lastName
                compare_test, name, wratio = util.name_compare_list(student_name, recipient_list)
                # print(compare_test, name, wratio)
                if not compare_test:
                    print(firstName + ' ' + lastName + ': Student did not receive award last year')

                else:
                    if GPA_Value:
                        GPA_Value = float(GPA_Value)
                        if GPA_Value < 2.75:
                            print(lastName, firstName, 'GPA is below 2.75. GPA is ' + str(GPA_Value))
                        elif GPA_Value < 2.9:
                            print(lastName, firstName, 'GPA is below 2.9, consider warning. GPA is ' + str(GPA_Value))
                    if major_school_change and re.sub('[^A-Za-z0-9]+', '', major_school_change.strip().upper()) not in [
                        'NO', 'NA']:
                        print(
                                firstName + ' ' + lastName + ': Major or School Change, investigate: ' + major_school_change)
                    if major == 'Not listed' and NON_ENG_value:
                        print(
                                firstName + ' ' + lastName + ': Other Major Listed, validate it is engineering: ' + NON_ENG_value)


def main():
    """
    The main function which runs the program
    """
    filename = 'Student Answers for 2020 Incentive Awards.csv'
    compute_HS_scores(filename)
    compute_C_scores(filename)


main()
