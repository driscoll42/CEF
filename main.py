import csv

import numpy as np
from scipy.stats import percentileofscore

import util

# TODO: Add documentation for functions and such

# TODO: Add gitignore with emails and passwords

# TODO: Package numpy, scipy

# TODO: Move these and other long variables to a csv
questions = {'lastName': 'LastName',
             'firstName': 'FirstName',
             'GPA_Value': 'Current Cumulative GPA out of a 4.0 scale (current term and year)',
             'ACT_SAT_value':
                 'What is your ACT or SAT score? (List the total score you wish to report, no need to specify if it is ACT or SAT)',
             'ACTM_SATM_value':
                 'What is your SAT or ACT Math score?',
             'COMMS_value': 'How many total community service hours have your completed during your high school career?',
             'NON_ENG_value': 'What is your expected major starting Fall 2020?',
             'student_type': 'What scholarship award are you applying for?'
             }


# TODO: Extract csv from AwardSpring automatically

def compute_HS_scores(file):
    # Values for some sanity checks
    min_SAT = 400
    max_SAT = 1600
    min_SATM = 200
    max_SATM = 800

    high_scooler = 'I am applying as a graduating high school senior in 2020 (I will be a freshman in college in Fall 2020).'

    # Load the conversion factors into a dict to reduce the number of times we have to iterate over the files
    SAT_to_ACT_dict = util.conversion_dict('SAT_to_ACT.csv')
    SAT_to_ACT_Math_dict = util.conversion_dict('SAT_to_ACT_Math.csv')

    # Create arrays to store the total for each ACT score type to determine precentiles
    ACT_Overall = []
    ACTM_Overall = []

    # Iterate through file once to get data for histograms and check high schooler(?)
    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            student_type = line[questions['student_type']]
            ACT_SAT_value = line[questions['ACT_SAT_value']]
            ACTM_SATM_value = line[questions['ACTM_SATM_value']]
            if student_type == high_scooler:
                ACT_score = util.ACT_SAT_Conv(ACT_SAT_value, SAT_to_ACT_dict, min_SAT, max_SAT)
                # Don't want to add the error values into our histogram and frankly only worth considering those which meet our mininum
                if ACT_score > 21:
                    ACT_Overall.append(ACT_score)
                ACTM_Score = util.ACT_SAT_Conv(ACTM_SATM_value, SAT_to_ACT_Math_dict, min_SATM, max_SATM)
                # Don't want to add the error values into our histogram and frankly only worth considering those which meet our mininum
                if ACTM_Score > 21:
                    ACTM_Overall.append(ACTM_Score)

    print("\n50th Percentile of arr, axis = None : ",
          np.percentile(ACT_Overall, 50))
    for x in reversed(range(22, 37)):
        print(x, ACT_Overall.count(x), percentileofscore(ACT_Overall, x))
    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames

        # Check if the questions exist in the file, most often a change in the year
        all_q_exist = True
        for q in questions.values():
            if q not in headers:
                print('ERROR: The following question is not in the headers, check for typos:')
                print(q)
                all_q_exist = False
        if not all_q_exist:
            return

        # TODO: Check submission status, if they have not submitted by filled everything out
        for line in d_reader:
            lastName = line[questions['lastName']]
            firstName = line[questions['firstName']]
            GPA_Value = line[questions['GPA_Value']]
            ACT_SAT_value = line[questions['ACT_SAT_value']]
            ACTM_SATM_value = line[questions['ACTM_SATM_value']]
            COMMS_value = line[questions['COMMS_value']]
            NON_ENG_value = line[questions['NON_ENG_value']]
            student_type = line[questions['student_type']]
            # TODO: Add Warnings based on residency
            # TODO: Add Distance and time between home and work
            # TODO: API to pull in socio-economic data of home zip
            # TODO: College accrediation check
            # TODO: Coursework functionality
            # TODO: Add high schools and unversities to AwardSpring
            # TODO: Overall error handling
            # TODO: Check for completed but unsubmitted applications
            if 0 == 1 and student_type == high_scooler and GPA_Value and ACT_SAT_value and ACTM_SATM_value and COMMS_value:
                GPA_Score = util.GPA_Calc(GPA_Value)
                ACT_SAT_Score = util.ACT_SAT_Calc(ACT_SAT_value, SAT_to_ACT_dict, min_SAT, max_SAT)
                # TODO: Improve the error handling here
                if ACT_SAT_Score == -1:
                    print(ACT_SAT_value, 'No conversion factor exists for this score (is it a decmial?)')
                elif ACT_SAT_Score == -2:
                    print(ACT_SAT_value, 'This score is too low for the SAT and too high for the ACT, check if correct')
                elif ACT_SAT_Score == -3:
                    print(ACT_SAT_value, 'This score is too high for the SAT, check if correct')
                ACTM_SATM_Score = util.ACT_SAT_Calc(ACTM_SATM_value, SAT_to_ACT_Math_dict, min_SATM, max_SATM)
                # TODO: Improve the error handling here
                if ACTM_SATM_Score == -1:
                    print(ACTM_SATM_value, 'No conversion factor exists for this score (is it a decmial?)')
                elif ACTM_SATM_Score == -2:
                    print(ACTM_SATM_value,
                          'This score is too low for the SAT and too high for the ACT, check if correct')
                elif ACTM_SATM_Score == -3:
                    print(ACTM_SATM_value, 'This score is too high for the SAT, check if correct')
                COMMS_Score = util.COMMS_calc(COMMS_value)
                if NON_ENG_value:
                    print('Potential non-engineering major, check: ' + NON_ENG_value)

                print(lastName + ', ' + firstName + ':', GPA_Score, ACT_SAT_Score, ACTM_SATM_Score, COMMS_Score)

                # TODO: Write back to Excel File or Google Spreadsheets
                # TODO: Send email with new students and warnings
        # TODO: Import reviewer scores and add the two together
        # TODO: Normalize reviewer scores

def compute_C_scores(file):
    # TODO: Don't start this for a while for lessons learned from HS
    # TODO: Check if past recipient
    # TODO: Check if changed university/major
    college_student = 'I am applying as a returning college student in 2019 (I will be a sophomore, junior, or senior in Fall 2019).'

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            student_type = line[questions['student_type']]
            lastName = line[questions['lastName']]
            firstName = line[questions['firstName']]
            GPA_Value = line[questions['GPA_Value']]

            if student_type == college_student:
                if GPA_Value:
                    GPA_Value = float(GPA_Value)
                    if GPA_Value < 2.75:
                        print(lastName, firstName, 'GPA is below 2.75. GPA is ' + str(GPA_Value))
                    elif GPA_Value < 2.9:
                        print(lastName, firstName, 'GPA is below 2.9, consider warning. GPA is ' + str(GPA_Value))
    return 0


filename = 'Student_Answers_2019.csv'
compute_HS_scores(filename)
# TODO: Finish compute_C_scores
# compute_C_scores(filename)
