import csv

import numpy as np
from scipy.stats import percentileofscore

import constants as cs
import util


# TODO: Add documentation for functions and such
# TODO: Add gitignore with emails and passwords, student data
# TODO: Package numpy, scipy
# TODO: Extract csv from AwardSpring automatically

def compute_HS_scores(file):
    # Load the conversion factors into a dict to reduce the number of times we have to iterate over the files
    SAT_to_ACT_dict = util.conversion_dict('SAT_to_ACT.csv')
    SAT_to_ACT_Math_dict = util.conversion_dict('SAT_to_ACT_Math.csv')

    # Iterate through file once to get data for histograms
    ACT_Overall, ACTM_Overall = util.generate_histo_arrays(file, SAT_to_ACT_dict, SAT_to_ACT_Math_dict)

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
        for q in cs.questions.values():
            if q not in headers:
                print('ERROR: The following question is not in the headers, check for typos:')
                print(q)
                all_q_exist = False
        if not all_q_exist:
            return

        # TODO: Check submission status, if they have not submitted by filled everything out
        for line in d_reader:
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]
            GPA_Value = line[cs.questions['GPA_Value']]
            ACT_SAT_value = line[cs.questions['ACT_SAT_value']]
            ACTM_SATM_value = line[cs.questions['ACTM_SATM_value']]
            COMMS_value = line[cs.questions['COMMS_value']]
            NON_ENG_value = line[cs.questions['NON_ENG_value']]
            student_type = line[cs.questions['student_type']]
            # TODO: Add Warnings based on residency, use https://smartystreets.com/
            # TODO: Add Distance and time between home and work
            # TODO: API to pull in socio-economic data of home zip
            # TODO: College accrediation check
            # TODO: Coursework functionality
            # TODO: Add high schools and unversities to AwardSpring
            # TODO: Overall error handling
            # TODO: Check for completed but unsubmitted applications
            if 0 == 1 and student_type == cs.high_scooler and GPA_Value and ACT_SAT_value and ACTM_SATM_value and COMMS_value:
                GPA_Score = util.GPA_Calc(GPA_Value)
                ACT_SAT_Score = util.ACT_SAT_Calc(ACT_SAT_value, SAT_to_ACT_dict)
                # TODO: Improve the error handling here
                if ACT_SAT_Score == -1:
                    print(ACT_SAT_value, 'No conversion factor exists for this score (is it a decmial?)')
                elif ACT_SAT_Score == -2:
                    print(ACT_SAT_value, 'This score is too low for the SAT and too high for the ACT, check if correct')
                elif ACT_SAT_Score == -3:
                    print(ACT_SAT_value, 'This score is too high for the SAT, check if correct')
                ACTM_SATM_Score = util.ACT_SAT_Calc(ACTM_SATM_value, SAT_to_ACT_Math_dict)
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

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            student_type = line[cs.questions['student_type']]
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]
            GPA_Value = line[cs.questions['GPA_Value']]

            if student_type == cs.college_student:
                if GPA_Value:
                    GPA_Value = float(GPA_Value)
                    if GPA_Value < 2.75:
                        print(lastName, firstName, 'GPA is below 2.75. GPA is ' + str(GPA_Value))
                    elif GPA_Value < 2.9:
                        print(lastName, firstName, 'GPA is below 2.9, consider warning. GPA is ' + str(GPA_Value))
    return 0


def main():
    filename = 'Student_Answers_2019.csv'
    compute_HS_scores(filename)
    # TODO: Finish compute_C_scores
    # compute_C_scores(filename)


main()
