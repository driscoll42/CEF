# Chicago Engineers' Foundation Scholarship Validation and Scoring Program

This program is built to automate the validation of the eligibility of applicants to the Chicago Engineers' Foundation award and to score their applications. The scoring and qualifications for the award are determined the the Awards Committee and the Board of Director's of the CEF. The goal of this program is to reduce the overhead spent on checking the students and to remove the rote work of the reviewers in looking at tables to determine a score for GPA, as well as to provide more accuracy, fewer errors, and reduce bias in the reviews. 

Website: https://www.chicagoengineersfoundation.org/

## High School Validation Features

* Checks if the home address listed is a residential address or a business address (uses USPS data)
* Checks if the University + Major are ABET accredited. If the major is Undecided, just checks the University
* Checks if the major is a non-engineering major 
* Check if home address is not Chicago that the school is a Chicago High School
* Check if student has filled out their application but not yet submitted it (WIP)

## College Validation Features

* Checks if student received the CEF award in the prior year
* Checks if student's GPA is too long for the award or close to the cut off
* Checks if the student's school or major has changed from engineering
* Check if student has filled out their application but not yet submitted it (WIP)

## Scoring Features
See scoring_util ReadMe for technical details

* Scores GPA based on percentile bracketing
* Converts SAT Scores to equivalent ACT scores
* Scores ACT and ACT Math on percentile bracketing
* Determines reviewers are overly harsh or generous and compensates
* Scores the student's STEM coursework (WIP)

## Awards Determination Features

* Determine the quality of the school (WIP)
* Determine distance between school and home address

## Automation Features

* Extract csv from AwardSpring automatically (WIP)
* Packaged necessary packages for ease of install (WIP)
* Host code on AWS (WIP)
* Generate email with new students and validation warnings when program runs (WIP)
* Write back data to a Google Spreadsheet  (WIP)

# Other Features

* When comparing names (e.g. high school, university or student names) to a list, uses fuzzy logic to account for misspellings and nicknames

## Misc TODOs

* Implement Sphninx (WIP)
* Add gitignore with emails and passwords, better secure them (WIP)

##  Changes for next year's award
* Make the ACT/SAT/GPA questions numeric (WIP)
* Ask students for the address of their school (too many have the same name) (WIP)
* Reword the STEM classes question to ask for just all math and science classes
* Make uploading the transcript more critical
* Ask for extracurriculars
* Ask for ACT/SAT Superscores

## Long Term TODOs

* Download student's ACT/SAT report and validate
* Download student's transcript and scrape coursework off of it
* Automate emails sending to students to remind them to finish application

## Install Instructions

* Create an Anaconda 3.7 python environment
* Run "pip install numpy, scipy, smartystreets_python_sdk, fuzzywuzzy"
* Run "conda install python-levenshtein"
* Then run the main.py

# How to Run

* After installing, download the latest "Student Answers" from AwardSpring into the Student_Data folder
* Ensure all the questions in the constants.py file match the questions in the downloaded csv
* Run main.py

## Release History

* 0.1.0
    * The first proper release
    * All basic validation features are functioning along with scoring (except STEM)