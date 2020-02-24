import numpy as np
import statistics as stat
import math
import csv
import constants as cs


# To run this the student names MUST be concatenated together in the order "LastNameFirstName"
# For example if FirstName = John and LastName = Doe, then student1 = DoeJohn
# Currently it works if a reviewer has a z score, for all students, greater or less than 1/-1 for all test students
#
def get_reviewer_scores_normalized(file, student1, student2, student3):
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
    student1_std = 0
    student2_std = 0
    student3_std = 0
    all_scores = {}
    harsh_reviewer = []
    generous_reviewer = []
    reviewer_output = {}

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames
        for line in d_reader:
            ReviewerLastName = line[cs.ReviewerLastName]
            ReviewerFirstName = line[cs.ReviewerFirstName]
            StudentLastName = line[cs.StudentLastName]
            StudentFirstName = line[cs.StudentFirstName]
            GivenScore = float(line[cs.GivenScore])
            ReviewStatus = line[cs.ReviewStatus]

            student = StudentLastName + StudentFirstName
            reviewer = ReviewerLastName + ReviewerFirstName
            if reviewer not in reviewer_list:
                reviewer_list.append(reviewer)

            if student == student1:
                student1_dict[reviewer] = GivenScore
                student1_arr.append(GivenScore)
                review1_dict[reviewer] = GivenScore
            elif student == student2:
                student2_dict[reviewer] = GivenScore
                student2_arr.append(GivenScore)
                review2_dict[reviewer] = GivenScore
            elif student == student3:
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


print(get_reviewer_scores_normalized('NormalizeTest.csv', 'User 1Test', 'User 2Test',
                                     'User 3Test'))


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
