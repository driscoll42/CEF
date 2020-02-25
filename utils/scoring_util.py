"""
All functions related to generating the score for each applicant
"""

import csv
import math
import statistics as stat
from typing import Tuple

import numpy as np
from scipy.stats import percentileofscore

import constants as cs
from utils import util


# To run this the student names MUST be concatenated together in the order "LastNameFirstName"
# For example if FirstName = John and LastName = Doe, then student1 = DoeJohn
# Currently it works if a reviewer has a z score, for all students, greater or less than 1/-1 for all test students
#
def get_reviewer_scores_normalized(file: str) -> dict:
    """

    Parameters
    ----------
    file : str
        The name of the file which contains the reviewer scores

    Returns
    -------
    object

    """
    reviewer_list = []
    student1_dict = {}
    student1_arr = []
    review1_dict = {}
    student2_dict = {}
    student2_arr = []
    review2_dict = {}
    student3_dict = {}
    student3_arr = []
    review3_dict = {}
    all_scores = {}
    harsh_reviewer = []
    generous_reviewer = []
    reviewer_output = {}

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            ReviewerLastName = line[cs.ReviewerLastName]
            ReviewerFirstName = line[cs.ReviewerFirstName]
            StudentLastName = line[cs.StudentLastName]
            StudentFirstName = line[cs.StudentFirstName]
            GivenScore = float(line[cs.GivenScore])
            ReviewStatus = line[cs.ReviewStatus]

            if ReviewStatus == 'Complete':
                student = StudentLastName + StudentFirstName
                reviewer = ReviewerLastName + ReviewerFirstName
                if reviewer not in reviewer_list:
                    reviewer_list.append(reviewer)

                if student == cs.student1:
                    student1_dict[reviewer] = GivenScore
                    student1_arr.append(GivenScore)
                    review1_dict[reviewer] = GivenScore
                elif student == cs.student2:
                    student2_dict[reviewer] = GivenScore
                    student2_arr.append(GivenScore)
                    review2_dict[reviewer] = GivenScore
                elif student == cs.student3:
                    student3_dict[reviewer] = GivenScore
                    student3_arr.append(GivenScore)
                    review3_dict[reviewer] = GivenScore
                if student not in all_scores.keys():
                    all_scores[student] = [[reviewer, GivenScore]]
                else:
                    all_scores[student].append([reviewer, GivenScore])

    student1_avg = stat.mean(student1_arr)
    student2_avg = stat.mean(student2_arr)
    student3_avg = stat.mean(student3_arr)
    student1_std = float(np.std(np.array(student1_arr)))
    student2_std = float(np.std(np.array(student2_arr)))
    student3_std = float(np.std(np.array(student3_arr)))

    for r in reviewer_list:
        student1_z = round((review1_dict[r] - student1_avg) / student1_std, 2)
        student2_z = round((review2_dict[r] - student2_avg) / student2_std, 2)
        student3_z = round((review3_dict[r] - student3_avg) / student3_std, 2)
        if student1_z > 1 and student2_z > 1 and student3_z > 1:
            print(r, student1_z, student2_z, student3_z)
            generous_reviewer.append(reviewer)
        if student1_z < -1 and student2_z < -1 and student3_z < -1:
            print(r, student1_z, student2_z, student3_z)
            harsh_reviewer.append(reviewer)

    for s in all_scores:
        n = len(all_scores[s])
        for i, review in enumerate(all_scores[s]):
            if review[0] in harsh_reviewer:
                if s not in reviewer_output:
                    reviewer_output[s] = review[1] + (student1_std + student2_std + student3_std) / 3
                else:
                    reviewer_output[s] = reviewer_output[s] + (
                            (review[1] + (student1_std + student2_std + student3_std) / 3) - reviewer_output[s]) / n
            elif review[0] in generous_reviewer:
                if s not in reviewer_output:
                    reviewer_output[s] = review[1] - (student1_std + student2_std + student3_std) / 3
                else:
                    reviewer_output[s] = reviewer_output[s] + (
                            (review[1] - (student1_std + student2_std + student3_std) / 3) - reviewer_output[s]) / n
            else:
                if s not in reviewer_output:
                    reviewer_output[s] = review[1] - (student1_std + student2_std + student3_std) / 3
                else:
                    reviewer_output[s] = reviewer_output[s] + (
                            (review[1] - (student1_std + student2_std + student3_std) / 3) - reviewer_output[s]) / n

    return reviewer_output


# print(get_reviewer_scores_normalized('NormalizeTest.csv', 'User 1Test', 'User 2Test',                                     'User 3Test'))


def get_reviewer_scores(file: str) -> dict:
    """

    Parameters
    ----------
    file

    Returns
    -------

    """
    reviewer_avg = {}
    student_cnt = {}

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            lastName = line['StudentLastName']
            firstName = line['StudentFirstName']
            score = float(line['GivenScore'])

            concat_name = lastName.strip().upper() + firstName.strip().upper()
            if concat_name in student_cnt:
                student_cnt[concat_name] = student_cnt[concat_name] + 1
            else:
                student_cnt[concat_name] = 1

            if concat_name in reviewer_avg:
                reviewer_avg[concat_name] = reviewer_avg[concat_name] + (score - reviewer_avg[concat_name]) / \
                                            student_cnt[concat_name]
            else:
                reviewer_avg[concat_name] = score

    return reviewer_avg


def generate_histo_arrays(file: str, SAT_to_ACT_dict: dict, SAT_to_ACT_Math_dict: dict) -> Tuple[list, list]:
    """

    Parameters
    ----------
    file : str
    SAT_to_ACT_dict : dict
    SAT_to_ACT_Math_dict : dict

    Returns
    -------
    ACT_Overall : list
    ACTM_Overall : list

    """
    # Create arrays to store the total for each ACT score type to determine percentiles
    ACT_Overall = []
    ACTM_Overall = []

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            student_type = line[cs.questions['student_type']]

            ACT_SAT_value = util.get_num(line[cs.questions['ACT_SAT_value']])
            ACTM_SATM_value = util.get_num(line[cs.questions['ACTM_SATM_value']])

            if cs.high_schooler in student_type.upper():
                ACT_score = ACT_SAT_Conv(ACT_SAT_value, SAT_to_ACT_dict)
                # Don't want to add the error values into our histogram and frankly only worth considering those which meet our minimum
                if ACT_score > 21:
                    ACT_Overall.append(ACT_score)
                ACTM_Score = ACT_SAT_Conv(ACTM_SATM_value, SAT_to_ACT_Math_dict)
                # Don't want to add the error values into our histogram and frankly only worth considering those which meet our minimum
                if ACTM_Score > 21:
                    ACTM_Overall.append(ACTM_Score)
    return ACT_Overall, ACTM_Overall


def GPA_Calc(gpa: float) -> float:
    """

    Parameters
    ----------
    gpa

    Returns
    -------

    """
    # If over 4 assume out of 5.0 scale, if over 5.0 assume 6.0
    if math.ceil(gpa) == 5:
        gpa = 4.0 * gpa / 5.0
    elif math.ceil(gpa) == 6:
        gpa = 4.0 * gpa / 6.0

    # 2.91 is worth 1 point and every 0.10 is an extra point up to 10 points
    GPA_Score = gpa
    GPA_Score -= 2.90
    GPA_Score = max(GPA_Score, 0)
    GPA_Score *= 10
    GPA_Score = math.ceil(GPA_Score)

    return GPA_Score


# It's easier to work in terms of ACT score and to convert everything to the same scale
# Source: https://www.act.org/content/dam/act/unsecured/documents/ACT-SAT-Concordance-Tables.pdf

def ACT_SAT_Conv(score: float, conv_dict: dict) -> int:
    """

    Parameters
    ----------
    score
    conv_dict

    Returns
    -------

    """
    # Sanity checks for min/max scores
    if 36 < score < cs.min_SAT:
        return -2
    elif cs.max_SAT < score:
        return -3

    if score > 36:
        try:
            score = conv_dict[score]
        except:
            return -1
    return score


def ACT_SAT_Calc(value: float, conv_dict: dict, total_score: float, histogram: list) -> float:
    """

    Parameters
    ----------
    value : float
    conv_dict : dict
    total_score : float
    histogram : list

    Returns
    -------
    total_score : float

    """
    ACT_SAT = ACT_SAT_Conv(value, conv_dict)

    if ACT_SAT == 36:  # Special case to give a few extra bonus fractions to perfect scores
        return total_score
    else:
        return total_score * percentileofscore(histogram, ACT_SAT) / 100


def class_split(classes: list) -> list:
    """WIP: A function that cleans an input list of classes the student has taken

    Parameters
    ----------
    classes : list
        A raw list of classes the student has taken

    Returns
    -------
    class_list : list
        The input list cleaned up to be standardized for scoring

    """
    classes = classes.replace(':', '')

    classes = classes.replace('w/', 'with')
    classes = classes.replace(' and ', ' & ')
    classes = classes.replace('Adv.', 'Advanced')
    classes = classes.replace('Trigonometry', 'Trig')

    classes = classes.replace('A.P.', 'AP')
    classes = classes.replace(' AP', ',AP')
    classes = classes.replace(' AP', ',AP')
    classes = classes.replace(' A.P.', ',AP')
    classes = classes.replace(' Ap ', ',AP ')

    classes = classes.replace(' IB', ',IB')

    classes = classes.replace(' Honors', ',Honors')
    classes = classes.replace(' Honor', ',Honors')
    classes = classes.replace(' HS', ',Honors')
    classes = classes.replace(' HS1', ',Honors')
    classes = classes.replace('Honors1', 'Honors')
    classes = classes.replace(' H ', ',Honors ')
    classes = classes.replace(' H-', ',Honors')
    classes = classes.replace(' (Honors)', ',Honors')
    classes = classes.replace(' (H)', ',Honors')

    classes = classes.replace(' Dual-Credit', ',Dual-Credit')
    classes = classes.replace(' Dual Credit', ',Dual-Credit')

    classes = classes.replace(' College Credit', ',College Credit')

    classes = classes.replace('A.P.', 'AP')

    classes = classes.replace(' I ', ' 1 ')
    classes = classes.replace(' I,', ' 1,')
    classes = classes.replace(' II ', ' 2 ')
    classes = classes.replace(' II,', ' 2,')
    classes = classes.replace(' III ', ' 3 ')
    classes = classes.replace(' III,', ' 3,')
    classes = classes.replace(' IV ', ' 4 ')
    classes = classes.replace(' IV,', ' 4,')
    classes = classes.replace(' V ', ' 5 ')
    classes = classes.replace(' V,', ' 5,')
    classes = classes.replace(' 1 ', ' 1,')
    classes = classes.replace(' 2 ', ' 2,')
    classes = classes.replace(' 3 ', ' 3,')
    classes = classes.replace(' 4 ', ' 4,')
    classes = classes.replace(' 5 ', ' 5,')

    classes = classes.replace('. , ', ',')
    classes = classes.replace('.)', ',')
    classes = classes.replace(' - ', ',')
    classes = classes.replace(' -', ',')
    classes = classes.replace(',,', ',')

    class_list = classes.split(',')

    return class_list


def COMMS_calc(value: float) -> int:
    """Converts total community service hours into a score

    Parameters
    ----------
    value : float
        A number designating the number of community service hours the applicant has done

    Returns
    -------
    COMMS_Score : int
        An integer score

    """
    if value > 100:
        COMMS_Score = 5
    elif value > 90:
        COMMS_Score = 4
    elif value > 80:
        COMMS_Score = 3
    elif value > 70:
        COMMS_Score = 2
    elif value > 60:
        COMMS_Score = 1
    else:
        COMMS_Score = 0

    return COMMS_Score
