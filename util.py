import csv
import math


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
    if not value:
        GPA = 0
    else:
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

def ACT_SAT_Conv(score, conv_dict, min_SAT, max_SAT):
    if not score:
        score = 0
    else:
        score = int(score)

    # Sanity checks for min/max scores
    if 36 < score < min_SAT:
        return -2
    elif max_SAT < score:
        return -3

    if score > 36:
        try:
            score = conv_dict[score]
        except:
            return -1
    return score

def ACT_SAT_Calc(value, conv_dict, min_SAT, max_SAT):

    ACT_SAT = ACT_SAT_Conv(value, conv_dict, min_SAT, max_SAT)

    # TODO: Determine percentiles
    if ACT_SAT <= 36:
        ACT_SAT -= 21
        ACT_SAT_Score = max(ACT_SAT, 0)
    else:
        ACT_SAT_Score = 0

    return ACT_SAT_Score


def COMMS_calc(value):
    if not value:
        COMMS = 0
    else:
        COMMS = float(value)

    COMMS_Score = 0

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

    return COMMS_Score
