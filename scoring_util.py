import numpy as np
import math
import csv
import constants as cs

def reviewer_normalize(file, student1, student2, student3):
    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames




reviewer_normalize('NormalizeTest.csv', 'User 3Test', 'User 1Test', 'User 2Test')



def get_reviewer_scores(file):
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