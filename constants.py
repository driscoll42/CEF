"""
This file contains constants that are used in the other files to provide one source.

It is intended for this one day to be in a non-developer accessible spreadsheet for ease of maintenance
"""
# TODO: Move these and other long variables outside of a py file so a non-technical user can edit them
# TODO: Figure out how to handle the questions changing

questions = {'lastName': 'LastName',
             'firstName': 'FirstName',
             'GPA_Value': 'Current Cumulative GPA out of a 4.0 scale (current term and year)',
             'ACT_SAT_value':
                 'What is your ACT or SAT score? (List the total score you wish to report, no need to specify if it is ACT or SAT)',
             'ACTM_SATM_value':
                 'What is your SAT or ACT Math score?',
             'COMMS_value': 'How many total community service hours have you completed during your high school career?',
             'NON_ENG_value': 'What is your expected major starting Fall 2020?',
             'student_type': 'What scholarship award are you applying for?',
             'other_major': 'What is your expected major starting Fall 2020?',
             'major_school_change': 'Has your major or university changed since you received your last CEF award?  If YES, please provide details. If not, please leave this field blank.',
             'STEM_Classes': 'List the STEM-related (Science, Technology, Engineering, and Math) courses you have taken that you feel are preparing you for an engineering career. Please separate each class with a comma, and only list courses in this section. (For Example: Honors Algebra 1, Honors Algebra 2, AP Physics C, IB Biology, Pre-Calculus, etc...) If you wish to elaborate on the courses or add additional information, please do so below in the "Use this space to add other details" section at the bottom of this form.',
             'College': 'What university will you be attending for the 2020-2021 school year?',
             'Other_College': 'List the official name of the university you are attending',
             'address1': 'Home Address (please provide best address to contact you)',
             'address2': 'Address Line 2 (E.g. Apt #, Suite #, Unit #, Floor #, etc...)',
             'city': 'City',
             'zip': 'Zip Code',
             'country': 'Country',
             'state': 'State',
             'high_school': 'What high school did you attend?',
             'high_school_other': 'Name of your high school'
             }

questions_2019 = {'lastName'           : 'LastName',
                  'firstName'          : 'FirstName',
                  'GPA_Value'          : 'Current Cumulative GPA out of a 4.0 scale (current term and year)',
                  'ACT_SAT_value'      :
                      'What is your ACT or SAT score? (List the total score you wish to report, no need to specify if it is ACT or SAT)',
                  'ACTM_SATM_value'    :
                      'What is your SAT or ACT Math score?',
                  'COMMS_value'        : 'How many total community service hours have you completed during your high school career?',
                  'NON_ENG_value'      : 'What is your expected major starting Fall 2020?',
                  'student_type'       : 'What scholarship award are you applying for?',
                  'other_major'        : 'What is your expected major starting Fall 2020?',
                  'major_school_change': 'Has your major or university changed since you received your last CEF award?  If YES, please provide details. If not, please leave this field blank.',
                  'STEM_Classes'       : 'List the Honors, AP, IB or college-level Math or Science courses you completed in high school.',
                  'College'            : 'What university will you be attending for the 2020-2021 school year?',
                  'Other_College'      : 'List the official name of the university you are attending',
                  'address1'           : 'Home Address (please provide best address to contact you)',
                  'address2'           : 'Address 2',
                  'city'               : 'City',
                  'zip'                : 'Zip Code',
                  'country'            : 'Country',
                  'state'              : 'State',
                  'high_school'        : 'What high school did you attend?',
                  'high_school_other'  : 'Name of your high school'
                  }

questions_2018 = {'lastName': 'LastName',
                  'firstName': 'FirstName',
                  'GPA_Value': 'Current Cumulative GPA out of a 4.0 scale (current term and year) Please refer to the FAQ/Help for questions',
                  'ACT_SAT_value':
                      'What is your ACT or SAT Score? (Please use whichever you prefer to report)',
                  'ACTM_SATM_value':
                      'What is your SAT or ACT Math Score?',
                  'COMMS_value': 'How many community service hours have you completed?',
                  'NON_ENG_value': 'What is your expected major for the 2017-2018 school year?',
                  'student_type': 'What scholarship are you applying for?'
                  }

questions_2017 = {'lastName': 'LastName',
                  'firstName': 'FirstName',
                  'GPA_Value': 'Current Cumulative GPA out of a 4.0 scale (current term and year) Please refer to the FAQ/Help for questions',
                  'ACT_SAT_value':
                      'What is your ACT or SAT Score? (Please use whichever you prefer to report)',
                  'ACTM_SATM_value':
                      'What is your SAT or ACT Math Score?',
                  'COMMS_value': 'How many community service hours have you completed?',
                  'NON_ENG_value': 'What is your expected major for the 2017-2018 school year?',
                  'student_type': 'What type of student are you:'
                  }

uni_not_listed = 'My university is not listed'

# Values for some sanity checks
min_SAT = 400
max_SAT = 1600
min_SATM = 200
max_SATM = 800

# Various functions check for student types
high_schooler = 'HIGH SCHOOL SENIOR'
college_student = 'COLLEGE STUDENT'

# ABET Constants
abet_school_name = 'School Name'
abet_major = 'Program Name'

# Reviewer Constants
ReviewerLastName = 'ReviewerLastName'
ReviewerFirstName = 'ReviewerFirstName'
StudentLastName = 'StudentLastName'
StudentFirstName = 'StudentFirstName'
GivenScore = 'GivenScore'
ReviewStatus = 'ReviewStatus'

# Normalized students, LastName concatenated with FirstName
student1 = 'User 1Test'
student2 = 'User 2Test'
student3 = 'User 3Test'

# Website Constants
AS_URL = 'https://chicagoengineersfoundation.awardspring.com/'
