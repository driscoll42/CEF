"""
The main file for the project which runs by default validations for all high school and college applicants.
It also generates a score for each applicant based on predefined criteria.
"""

import csv
import time
from datetime import datetime
from typing import Tuple

import pandas as pd

import constants as cs
from classes import Student
from utils import validations as vali, scoring_util as sutil, util, unittests


# First ones to work on
# TODO: Add school address to spreadsheet
# TODO: Detect wide reviewer spread (lowest and highest is greater than 20? 25? points)
# TODO: If record doesn't write, throw up error
# TODO: Replace file logic with pandas

# Backlog
# TODO: Output data to Google Spreadsheets https://www.twilio.tcom/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html https://automatetheboringstuff.com/2e/chapter14/
# TODO: Coursework functionality
# TODO: Extract csv from AwardSpring automatically - https://automatetheboringstuff.com/2e/chapter12/
# https://realpython.com/python-web-scraping-practical-introduction/
# TODO: Implement Sphnix
# TODO: Move constants to Google Spreadsheet for non-dev user to update
# TODO: Email notifications for warnings
# TODO: Incremental changes
# TODO: Detect changes and update Google Sheet rather than rerunning every time
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
# TODO: Ask for SAT II test scores?
# TODO: batchgeo autogen?


def compute_HS_scores(year: int, verbose: bool = False, DEBUG: bool = False, CALL_APIS: bool = False):
    """The main function that computes the high school student's scores and validates their application

    Parameters
    ----------
    file : str
        The file with all of the student's answers

    Returns
    -------

    """
    file = f'Student Answers for {str(year)} Incentive Awards.csv'
    with open(f'Student_Data/{file}', 'r', encoding="utf-8-sig") as csvinput:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(csvinput)
        headers = d_reader.fieldnames
        # Check if the questions exist in the file, most often a change in the year
        if not vali.questions_check(headers, year):
            return

        # Adding leading columns for the scores the students recieved
        headers = ['Total', 'GPA', 'ACTSAT', 'ACTMSATM', 'STEM', 'Reviewer', 'CommServ', 'Essay', 'Career', 'Bonus',
                   'Notes', 'home_to_school_dist', 'home_to_school_time_pt', 'home_to_school_time_car', 'ACT_value',
                   'ACTM_value'] + d_reader.fieldnames

        writer = csv.DictWriter(open(f'{year}_output.csv', 'w', newline='', encoding='utf-8-sig'), fieldnames=headers)

        writer.writeheader()
        # Load the conversions and lists into variables for reuse
        SAT_to_ACT_dict = util.conversion_dict('SAT_to_ACT.csv', 'int')
        SAT_to_ACT_Math_dict = util.conversion_dict('SAT_to_ACT_Math.csv', 'int')
        course_scores = util.conversion_dict('Course_scoring.csv', 'str')
        school_list, chicago_schools = vali.get_school_list('Illinois_Schools_Fix.csv')

        if year >= 2022:  # Only started getting this in 2022
            reviewer_feedback_df = util.get_review_feedback(f'{year} CEF Reviewer Detailed Feedback.xlsx')

        # Iterate through file once to get data for histograms
        ACT_Overall, ACTM_Overall = sutil.generate_histo_arrays(file, SAT_to_ACT_dict, SAT_to_ACT_Math_dict, year)

        if year in cs.normalizing_students:
            reviewer_scores = sutil.get_reviewer_scores_normalized(
                    f'Reviewer Scores by Applicant for {str(year)} Incentive Awards.csv', year)
        else:
            reviewer_scores = sutil.get_reviewer_scores(f'Reviewer Scores by Applicant for {year} Incentive Awards.csv')
        student_list = []
        cnt = 0
        for line in d_reader:
            cnt += 1
            # if cnt > 2:
            #    break
            lastName = line[cs.questions[year][0]['lastName']].strip()
            firstName = line[cs.questions[year][0]['firstName']].strip()

            s = Student.Student(firstName, lastName)

            s.GPA_Value = util.get_num(line[cs.questions[year][0]['GPA_Value']])
            s.ACT_SAT_value = util.get_num(line[cs.questions[year][0]['ACT_SAT_value']])
            s.ACTM_SATM_value = util.get_num(line[cs.questions[year][0]['ACTM_SATM_value']])

            s.COMMS_value = util.get_num(line[cs.questions[year][0]['COMMS_value']])
            s.NON_ENG_value = line[cs.questions[year][0]['NON_ENG_value']]
            s.student_type = line[cs.questions[year][0]['student_type']]

            s.major = line['Major']
            s.other_major = line[cs.questions[year][0]['other_major']]
            s.STEM_Classes = line[cs.questions[year][0]['STEM_Classes']]

            s.College = line[cs.questions[year][0]['College']]
            s.Other_College = line[cs.questions[year][0]['Other_College']]
            s.high_school_full = line[cs.questions[year][0]['high_school']]
            s.high_school_other = line[cs.questions[year][0]['high_school_other']]

            if year >= 2021:
                s.submitted = line['Submit Application Complete']
            else:
                s.submitted = 'Yes'

            s.address1 = line[cs.questions[year][0]['address1']]
            s.address2 = line[cs.questions[year][0]['address2']]
            s.city = line[cs.questions[year][0]['city']]
            s.state = line[cs.questions[year][0]['state']]
            s.zip_code = line[cs.questions[year][0]['zip']]
            if CALL_APIS is False:
                s.cleaned_address1 = line[cs.questions[year][0]['address1']]
                s.cleaned_address2 = line[cs.questions[year][0]['address2']]
                s.cleaned_city = line[cs.questions[year][0]['city']]
                if s.cleaned_city != 'Chicago' and s.firstName == 'ChicagoSchoolNoCHome':
                    s.ChicagoHome = False
                    s.validationError = True
                s.cleaned_state = line[cs.questions[year][0]['state']]
                s.cleaned_zip_code = line[cs.questions[year][0]['zip']]

            # A basic sanity check that if the GPA and ACT values are populated, then the applicant is probably applying
            if 1 == 1 and cs.high_schooler in s.student_type.upper() and s.GPA_Value and s.firstName != 'Test' and s.submitted == 'Yes':
                # print(s.lastName, s.firstName)
                # Validate the applicant's address is residential and that they live or go to high school in Chicago
                vali.address_validation(s, chicago_schools, school_list, verbose, DEBUG, CALL_APIS)

                # Validate the applicant is accepted into an ABET engineering program
                vali.accred_check(s, verbose, DEBUG)

                # Validate the applicants ACT/SAT scores and score their GPA and ACT/SAT
                sutil.GPA_Calc(s, True)
                sutil.ACT_SAT_Calc(s, SAT_to_ACT_dict, ACT_Overall, 'C', verbose, DEBUG)
                sutil.ACT_SAT_Calc(s, SAT_to_ACT_Math_dict, ACTM_Overall, 'M', verbose, DEBUG)

                # Score the applicant's verbose
                sutil.score_coursework(s, course_scores, True)

                # Determine the reviewer scores for the applicant
                if lastName.strip().upper() + firstName.strip().upper() in reviewer_scores:
                    s.reviewer_score = cs.reviewer_multiplier * round(
                            reviewer_scores[lastName.strip().upper() + firstName.strip().upper()])
                else:
                    s.reviewer_score = 0
                if year >= 2022:
                    try:
                        s.comm_score = round(
                                reviewer_feedback_df[reviewer_feedback_df['Applicant_'] == f'{lastName}, {firstName}'][
                                    'Community Service / Work_mean'].values[0], 2)
                        s.essay_score = round(
                                reviewer_feedback_df[reviewer_feedback_df['Applicant_'] == f'{lastName}, {firstName}'][
                                    'Short Essay_mean'].values[0], 2)
                        # s.career_score = round(                                reviewer_feedback_df[reviewer_feedback_df['Applicant_'] == f'{lastName}, {firstName}'][                                    'Career Goals_mean'].values[0], 2)
                        s.bonus_score = round(
                                reviewer_feedback_df[reviewer_feedback_df['Applicant_'] == f'{lastName}, {firstName}'][
                                    'Bonus/Discretionary Points_mean'].values[0], 2)
                        s.notes = \
                            reviewer_feedback_df[reviewer_feedback_df['Applicant_'] == f'{lastName}, {firstName}'][
                                'Notes_join'].values[0]
                    except Exception as e:
                        print(lastName, e)
                        s.comm_score = 0
                        s.essay_score = 0
                        s.career_score = 0
                        s.bonus_score = 0
                        s.notes = ''
                if verbose:
                    print(
                        f'{lastName}, {firstName}: {s.GPA_Score} {s.ACT_SAT_Score} {s.ACTM_SATM_Score} {s.reviewer_score} {s.comm_score} {s.essay_score} {s.career_score} {s.bonus_score}')
                    pass


                # TODO: Send email with new students and warnings https://automatetheboringstuff.com/2e/chapter18/

                # Write back to output csv file
                total = s.GPA_Score + s.ACT_SAT_Score + s.ACTM_SATM_Score + s.reviewer_score + s.STEM_Score

                writer.writerow(dict(line,
                                     Total=total,
                                     GPA=s.GPA_Score,
                                     ACTSAT=s.ACT_SAT_Score,
                                     ACTMSATM=s.ACTM_SATM_Score,
                                     STEM=s.STEM_Score,
                                     Reviewer=s.reviewer_score,
                                     CommServ=s.comm_score,
                                     Essay=s.essay_score,
                                     Career=s.career_score,
                                     Bonus=s.bonus_score,
                                     Notes=s.notes,
                                     home_to_school_dist=s.home_to_school_dist,
                                     home_to_school_time_pt=s.home_to_school_time_pt,
                                     home_to_school_time_car=s.home_to_school_time_car,
                                     ACT_value=s.ACT_value,
                                     ACTM_value=s.ACTM_value
                                     ))
                student_list.append(s)
    return student_list


def compute_C_scores(file: str, year: int, verbose: bool = False, DEBUG: bool = False, CALL_APIS: bool = False):
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

        recipient_list = vali.get_past_recipients('2019 Recipients.csv', year)
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
                if vali.past_recipient(s, recipient_list, verbose, DEBUG):
                    # Validate GPA
                    vali.college_gpa(s, verbose, DEBUG)

                    # Validate that the recipient's college and major are still valid
                    vali.college_school_major(s, verbose, DEBUG)
                college_students.append(s)
    return college_students


def generate_student_data(file: str, verbose: bool = False, DEBUG: bool = False) -> Tuple[list, list]:
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
    # TODO: Remember to do the XGBoost on the missing ACTs
    """
    The main function which runs the program
    """
    # TODO: Iterate through the students here once and pass student class to the two functions
    run_test_data = False
    run_all_data = True
    create_copy = False

    DEBUG = True
    verbose = True

    # WARNING: If this is True it will call the Google and SmartyStreets API
    CALL_APIS = False
    # WARNING: If this is True it will call the Google and SmartyStreets API

    if run_test_data:
        filename = 'Validation_Students.csv'
        student_data_time = time.time()
        validation_HS = compute_HS_scores(filename, verbose, DEBUG, CALL_APIS)
        HS_Run = time.time()
        print('Runtime of HS Validation: ' + str(HS_Run - student_data_time))
        unittests.unit_tests(validation_HS, CALL_APIS)
        validation_C = compute_C_scores(filename, verbose, DEBUG, CALL_APIS)
        print('Runtime of College Validation: ' + str(time.time() - HS_Run))
        unittests.unit_tests(validation_C, CALL_APIS)
        print('--------------')

    if run_all_data:
        year = 2024
        if create_copy:
            filename = f'Student Answers for {str(year)} Incentive Awards.csv'
            df = pd.read_csv(f'Student_Data/{filename}')
            filename = f'Modified_{str(datetime.now().strftime("%Y%m%d%H%M%S"))}_{filename}'
            df.to_csv('Student_Data/' + 'copy_of_' + filename)

        start = time.time()
        # generate_student_data(filename)
        student_data_time = time.time()
        print('Runtime of student data split: ' + str(student_data_time - start))
        high_school_students = compute_HS_scores(year, verbose, DEBUG, CALL_APIS)

        HS_Run = time.time()
        print('Runtime of HS: ' + str(HS_Run - student_data_time))
        # college_students = compute_C_scores(filename, verbose, DEBUG, CALL_APIS)
        # print('Runtime of College: ' + str(time.time() - HS_Run))


main()
