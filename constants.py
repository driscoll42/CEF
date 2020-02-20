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

# Values for some sanity checks
min_SAT = 400
max_SAT = 1600
min_SATM = 200
max_SATM = 800

# Various functions check for student types
# TODO: Make this work for different years checking LIKE condition
college_student = 'I am applying as a returning college student in 2019 (I will be a sophomore, junior, or senior in Fall 2019).'
high_scooler = 'I am applying as a graduating high school senior in 2020 (I will be a freshman in college in Fall 2020).'
