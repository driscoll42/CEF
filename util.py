import csv
import math
import re
import constants as cs
import numpy as np
from scipy.stats import percentileofscore


# Too much of the data is dirty often times, this function gets the first number in a string, and returns it
# If there is no number, or it's NULL, it returns a 0
def get_num(input_text):
    """Returns the first number in a string."""

    list_of_nums = re.findall(r'\d+', input_text)
    if len(list_of_nums) == 0:
        return 0
    else:
        return list_of_nums[0]


def generate_histo_arrays(file, SAT_to_ACT_dict, SAT_to_ACT_Math_dict):
    # Create arrays to store the total for each ACT score type to determine precentiles
    ACT_Overall = []
    ACTM_Overall = []

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            student_type = line[cs.questions['student_type']]

            ACT_SAT_value = get_num(line[cs.questions['ACT_SAT_value']])
            ACTM_SATM_value = get_num(line[cs.questions['ACTM_SATM_value']])

            if cs.high_scooler in student_type.upper():
                ACT_score = ACT_SAT_Conv(ACT_SAT_value, SAT_to_ACT_dict)
                # Don't want to add the error values into our histogram and frankly only worth considering those which meet our mininum
                if ACT_score > 21:
                    ACT_Overall.append(ACT_score)
                ACTM_Score = ACT_SAT_Conv(ACTM_SATM_value, SAT_to_ACT_Math_dict)
                # Don't want to add the error values into our histogram and frankly only worth considering those which meet our mininum
                if ACTM_Score > 21:
                    ACTM_Overall.append(ACTM_Score)
    return ACT_Overall, ACTM_Overall


def get_past_recipients(file):
    recipient_list = []

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]
            recipient_list.append(lastName.strip().upper() + firstName.strip().upper())
    return recipient_list





def conversion_dict(file_name):
    # This function assumes your from value is in the first column of the csv and your to is in the second
    # Further it assumes the first column has not repeats
    # Also assumes that all the values in the table are integers
    with open('Conversions/' + str(file_name), 'r', encoding="utf-8-sig") as f:
        d_reader = csv.DictReader(f)

        # get fieldnames from DictReader object and store in list
        headers = d_reader.fieldnames
        dict = {}
        header_one = headers[0]
        header_two = headers[1]

        for line in d_reader:
            dict[int(line[header_one])] = int(line[header_two])

    return dict


def GPA_Calc(value):
    GPA = float(value)

    # If over 4 assume out of 5.0 scale, if over 5.0 assume 6.0
    if math.ceil(GPA) == 5:
        GPA = 4.0 * GPA / 5.0
    elif math.ceil(GPA) == 6:
        GPA = 4.0 * GPA / 6.0

    # 2.91 is worth 1 point and every 0.10 is an extra point up to 10 points
    GPA_Score = GPA
    GPA_Score -= 2.90
    GPA_Score = max(GPA_Score, 0)
    GPA_Score *= 10
    GPA_Score = math.ceil(GPA_Score)

    return GPA_Score


# It's easier to work in terms of ACT score and to convert everything to the same scale
# Source: https://www.act.org/content/dam/act/unsecured/documents/ACT-SAT-Concordance-Tables.pdf

def ACT_SAT_Conv(score, conv_dict):
    score = int(score)

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


def ACT_SAT_Calc(value, conv_dict, total_score, histogram):
    ACT_SAT = ACT_SAT_Conv(value, conv_dict)

    if ACT_SAT == 36:  # Special case to give a few extra bonus fractions to perfect scores
        return total_score
    else:
        return total_score * percentileofscore(histogram, ACT_SAT) / 100


def class_split(classes):
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

    classes = classes.replace('. , ',',')
    classes = classes.replace('.)', ',')
    classes = classes.replace(' - ', ',')
    classes = classes.replace(' -', ',')
    classes = classes.replace(',,', ',')

    class_list = classes.split(',')

    return class_list


def COMMS_calc(value):
    COMMS = float(value)

    if COMMS > 100:
        COMMS_Score = 5
    elif COMMS > 90:
        COMMS_Score = 4
    elif COMMS > 80:
        COMMS_Score = 3
    elif COMMS > 70:
        COMMS_Score = 2
    elif COMMS > 60:
        COMMS_Score = 1
    else:
        COMMS_Score = 0

    return COMMS_Score
