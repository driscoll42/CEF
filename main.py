"""
The main file for the project which runs by default validations for all high school and college applicants.
It also generates a score for each applicant based on predefined criteria.
"""

import csv
import time
from typing import Tuple

import constants as cs
from classes import Student
from utils import validations as vali, scoring_util as sutil, util


# TODO: Overall error handling
# TODO: Test cases for each error type and function   https://realpython.com/python-testing/
# TODO: Replace all csvs with Google Spreadsheets https://www.twilio.tcom/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html https://automatetheboringstuff.com/2e/chapter14/
# TODO: Coursework functionality
# TODO: Extract csv from AwardSpring automatically - https://automatetheboringstuff.com/2e/chapter12/

# TODO: Implement Sphnix
# TODO: Move constants to Google Spreadsheet for non-dev user to update

# TODO: Add DEBUG functionality
# TODO: Add Distance and time between home and work
# TODO: Determine school quality
# TODO: Check submission status, if they have not submitted but filled everything out, autowarn?
# TODO: Make High School And College student subclass
# TODO: Store several variables as class variables https://realpython.com/inheritance-composition-python/
# TODO: Host this on an AWS server ? https://realpython.com/python-sql-libraries/
# TODO: Verify ACT/SAT from pdf https://pypi.org/project/pdftotext/
# TODO: Extract coursework from pdf https://pypi.org/project/pdftotext/
# TODO: Figure out how to handle the questions changing
# TODO: Add gitignore with emails and passwords, better secure them
# TODO: Package numpy, scipy

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

        # TODO: Once live, use the normalized function
        # reviewer_scores = sutil.get_reviewer_scores_normalized('Reviewer Scores by Applicant for 2019 Incentive Awards.csv')
        reviewer_scores = sutil.get_reviewer_scores('Reviewer Scores by Applicant for 2019 Incentive Awards.csv')
        student_list = []

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

            # A basic saity check that if the GPA and ACT values are populated, then the applicant is probably applying
            if 1 == 1 and cs.high_schooler in s.student_type.upper() and s.GPA_Value and s.ACT_SAT_value and s.ACTM_SATM_value and s.COMMS_value:
                # Validate the applicant's address is residential and that they live or go to high school in Chicago
                vali.address_validation(s, chicago_schools, school_list)

                # Validate the applicant is accepted into an ABET engineering program
                vali.accred_check(s)

                # Validate the applicants ACT/SAT scores and score their GPA and ACT/SAT
                sutil.GPA_Calc(s)
                sutil.ACT_SAT_Calc(s, SAT_to_ACT_dict, ACT_Overall, 'C')
                sutil.ACT_SAT_Calc(s, SAT_to_ACT_Math_dict, ACTM_Overall, 'M')

                # Score the applicant's coursework
                sutil.score_coursework(s)

                # Determine the reviewer scores for the applicant
                if lastName.strip().upper() + firstName.strip().upper() in reviewer_scores:
                    s.reviewer_score = cs.reviewer_multiplier * round(
                            reviewer_scores[lastName.strip().upper() + firstName.strip().upper()])
                else:
                    s.reviewer_score = 0

                # print(lastName + ', ' + firstName + ':', GPA_Score, ACT_SAT_Score, ACTM_SATM_Score, reviewer_score)

                # TODO: Write back to Excel File or Google Spreadsheets
                # TODO: Send email with new students and warnings https://automatetheboringstuff.com/2e/chapter18/
            student_list.append(s)


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
        college_students = []

        for line in d_reader:
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]

            s = Student.Student(firstName, lastName)

            s.student_type = line[cs.questions['student_type']]
            s.GPA_Value = line[cs.questions['GPA_Value']]
            s.major_school_change = line[cs.questions['major_school_change']]
            s.major = line['Major']
            s.NON_ENG_value = line[cs.questions['NON_ENG_value']]

            if cs.college_student in s.student_type.upper():

                # Validate if the student is a past recipient, if not no point in other checks
                if vali.past_recipient(s, recipient_list):
                    # Validate GPA
                    vali.college_gpa(s)

                    # Validate that the recipient's college and major are still valid
                    vali.college_school_major(s)
            college_students.append(s)


def generate_student_data(file: str) -> Tuple[list, list]:
    """Run through the student file to generate a list of the students with their class variable set

    Parameters
    ----------
    file : str
        The file with all of the student's answers

    Returns
    -------
    high_school_students : list
        A list containing instances of the Student class of all the high school students
    college_students : list
        A list containing instances of the Student class of all the high school students

    """

    high_school_students = []
    college_students = []
    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames

        # Check if the questions exist in the file, most often a change in the year
        if not vali.questions_check(headers):
            return high_school_students, college_students

    return high_school_students, college_students


def main():
    """
    The main function which runs the program
    """
    # TODO: Iterate through the students here once and pass student class to the two functions
    filename = 'Student Answers for 2020 Incentive Awards.csv'
    start = time.time()
    # generate_student_data(filename)
    student_data_time = time.time()
    print('Runtime of student data split: ' + str(student_data_time - start))
    compute_HS_scores(filename)
    HS_Run = time.time()
    print('Runtime of HS: ' + str(HS_Run - student_data_time))
    compute_C_scores(filename)
    print('Runtime of College: ' + str(time.time() - HS_Run))


main()
