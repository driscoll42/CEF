"""
All functions related to generating the score for each applicant

get_reviewer_scores_normalized - returns a dict of normalized reviewer scores
get_reviewer_scores - returns the average score for each student in a dict
generate_histo_arrays - generates lists containing all the ACT and ACTM scores
GPA_Calc - Calculates the number of points a student gets for their GPA
ACT_SAT_Conv - Converts SAT scores to ACT scores
ACT_SAT_Calc - The scoring function for ACT and ACT Math
class_split - WIP: A function that cleans an input list of classes the student has taken
COMMS_calc - Converts total community service hours into a score

"""

import csv
import math
import statistics as stat
from typing import Tuple

import numpy as np
from scipy.stats import percentileofscore

import constants as cs
from classes import Student
from utils import util


# To run this the student names MUST be concatenated together in the order "LastNameFirstName"
# For example if FirstName = John and LastName = Doe, then student1 = DoeJohn
# Currently it works if a reviewer has a z score, for all students, greater or less than 1/-1 for all test students
#
def get_reviewer_scores_normalized(file: str) -> dict:
    """This function takes in a file with all the reviews for all students and normalizes them. It does this based on
    the prerequisite that all reviewers have been assigned the same three students to review in addition to others.
    The program will compute the z-score for each reviewer and student combo for the three in question (how many
    standard deviations they are from the student's mean score). If a reviewer is consistently one standard deviation
    or more away from the mean in a positive or negative direction we assume they are a generous or harsh reviewer and
    when returning the average score for each student adjust those reviewer scores by one half of the average standard
    deviation for the three students.

    Parameters
    ----------
    file : str
        The name of the file which contains the reviewer scores

    Returns
    -------
    reviewer_output : dict
        A dictionary of normalized reviewer scores

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
                    reviewer_output[s] = review[1] + (student1_std + student2_std + student3_std) / 3 / 2
                else:
                    reviewer_output[s] = reviewer_output[s] + (
                            (review[1] + (student1_std + student2_std + student3_std) / 3 / 2) - reviewer_output[s]) / n
            elif review[0] in generous_reviewer:
                if s not in reviewer_output:
                    reviewer_output[s] = review[1] - (student1_std + student2_std + student3_std) / 3 / 2
                else:
                    reviewer_output[s] = reviewer_output[s] + (
                            (review[1] - (student1_std + student2_std + student3_std) / 3 / 2) - reviewer_output[s]) / n
            else:
                if s not in reviewer_output:
                    reviewer_output[s] = review[1]
                else:
                    reviewer_output[s] = reviewer_output[s] + (
                            (review[1]) - reviewer_output[s]) / n

    return reviewer_output


def get_reviewer_scores(file: str) -> dict:
    """Returns the average score for each student in a dict

    Parameters
    ----------
    file : str
        The name of the file which contains the reviewer scores

    Returns
    -------
    reviewer_avg : dict
        A dictionary of averaged reviewer scores by student
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


def generate_histo_arrays(file: str, SAT_to_ACT_dict: dict, SAT_to_ACT_Math_dict: dict) -> Tuple[dict, dict]:
    """This function takes in a file with all student's ACT/SAT scores (Composite and Math) along with conversion dicts
    to convert SAT scores to ACT scores, and outputs two lists, with all the ACT (SAT's converted) and ACT Math scores
    in a list. This is used to generate histograms later on

    Parameters
    ----------
    file : str
        The file name containing the student's ACT/SAT scores
    SAT_to_ACT_dict : dict
        A dict containing what ACT score is equivalent to what SAT score (Composite)
    SAT_to_ACT_Math_dict : dict
        A dict containing what ACT score is equivalent to what SAT score (Math)

    Returns
    -------
    ACT_Overall : list
        A list of all applicants ACT scores, duplicates are not removed and does not list student
    ACTM_Overall : list
        A list of all applicants ACT Math scores, duplicates are not removed and does not list student

    """
    # Create arrays to store the total for each ACT score type to determine percentiles
    ACT_Overall = []
    ACTM_Overall = []

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            student_type = line[cs.questions['student_type']]
            s = Student.Student('Dummy', 'Student')
            s.ACT_SAT_value = util.get_num(line[cs.questions['ACT_SAT_value']])
            s.ACTM_SATM_value = util.get_num(line[cs.questions['ACTM_SATM_value']])

            if cs.high_schooler in student_type.upper():
                ACT_score = ACT_SAT_Conv(s, SAT_to_ACT_dict, 'C')
                # Don't want to add the error values into our histogram and frankly only worth considering those which meet our minimum
                if ACT_score > 21:
                    ACT_Overall.append(ACT_score)
                ACTM_Score = ACT_SAT_Conv(s, SAT_to_ACT_Math_dict, 'M')
                # Don't want to add the error values into our histogram and frankly only worth considering those which meet our minimum
                if ACTM_Score > 21:
                    ACTM_Overall.append(ACTM_Score)

    # Rather than return the lists, just return the dicts, better for performance and memory
    ACT_Overall_dict = {}
    ACTM_Overall_dict = {}
    for x in range(0, 37):
        ACT_Overall_dict[x] = percentileofscore(ACT_Overall, x)
        ACTM_Overall_dict[x] = percentileofscore(ACTM_Overall, x)

    return ACT_Overall_dict, ACTM_Overall_dict


# It's easier to work in terms of ACT score and to convert everything to the same scale
# Source: https://www.act.org/content/dam/act/unsecured/documents/ACT-SAT-Concordance-Tables.pdf

def ACT_SAT_Conv(s: Student, conv_dict: dict, test_type: str) -> int:
    """Converts SAT scores to ACT scores

    Parameters
    ----------
    student : Student
        A member of the student Class
    conv_dict : dict
        A conversion dict for SAT to ACT
    test_type : str
        'C' : Composite, 'M' : Math
    Returns
    -------
    score : int
        The score in ACT terms

    """
    if test_type == 'C':
        score = s.ACT_SAT_value
    elif test_type == 'M':
        score = s.ACTM_SATM_value

    # Sanity checks for min/max scores
    if 36 < score < cs.min_SAT:
        s.validationError = True
        s.ACT_SAT_low = False
        score = 0.0
    elif cs.max_SAT < score:
        s.validationError = True
        s.ACT_SAT_high = False
        score = 0.0
    if not score.is_integer():
        s.validationError = True
        s.ACT_SAT_decimal = False
        score = 0.0

    if score > 36:
        try:
            score = conv_dict[score]
        except:
            s.validationError = True
            s.ACT_SAT_conversion = False
            score = 0.0
    return score


def ACT_SAT_Calc(student: Student, conv_dict: dict, histogram: dict, test_type: str) -> None:
    """The scoring function for ACT and ACT Math. We multiply the percentile of their score by a total_score

    Parameters
    ----------
    student : Student
        A member of the student Class
    conv_dict : dict
        The conversion dict of SAT to ACT
    histogram : list
        A list of all ACT scores over all applicants
    test_type : str
        'C' : Composite, 'M' : Math

    Returns
    -------
    """
    ACT_SAT = 0
    # This may be a bit redundant, but I like breaking it up
    if test_type == 'C':
        ACT_SAT = ACT_SAT_Conv(student, conv_dict, test_type)
    elif test_type == 'M':
        ACT_SAT = ACT_SAT_Conv(student, conv_dict, test_type)

    if ACT_SAT == 36:  # Special case to give a few extra bonus fractions to perfect scores
        multiplier = 1
    elif ACT_SAT < 0:
        multiplier = ACT_SAT
    else:
        multiplier = round(histogram[ACT_SAT] / 100, 2)

    if test_type == 'C':
        student.ACT_SAT_Score = multiplier * cs.ACT_Score
    elif test_type == 'M':
        student.ACTM_SATM_Score = multiplier * cs.ACTM_Score


def GPA_Calc(student: Student) -> None:
    """Calculates the number of points a student gets for their GPA. Any GPA scores over 4 are assumed to be out of 5,
    and any over 5 are assumed to be out of 6. These are then turned into 4.0 scores. AFter that, 2.91 is worth 1 point
    and every 0.10 is an extra point up to 10 points

    Parameters
    ----------
    student : Student
        A member of the student Class

    """
    # If over 4 assume out of 5.0 scale, if over 5.0 assume 6.0
    if math.ceil(student.GPA_Value) == 5:
        student.GPA_Value = 4.0 * student.GPA_Value / 5.0
    elif math.ceil(student.GPA_Value) == 6:
        student.GPA_Value = 4.0 * student.GPA_Value / 6.0

    # 2.90 is worth 1 point and every 0.10 is an extra point up to 10 points
    student.GPA_Score = student.GPA_Value - 2.8
    student.GPA_Score = max(student.GPA_Score, 0)
    student.GPA_Score = min(student.GPA_Score, 1)
    student.GPA_Score *= cs.GPA_Score
    student.GPA_Score = round(student.GPA_Score, 2)


def score_coursework(s: Student) -> None:
    classes = class_split(s.STEM_Classes)


def class_split(classes: str) -> list:
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

    '''for x in classes:
        if

        if x.strip() not in unique_class:
            unique_class.append(x.strip())'''

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
