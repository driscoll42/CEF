class Student:
    """A student class to track values and validation failures"""

    def __init__(self, firstName, lastName):
        self.lastName = lastName
        self.firstName = firstName
        self.GPA_Value = 0
        self.ACT_SAT_value = 0
        self.ACTM_SATM_value = 0
        self.COMMS_value = 0
        self.NON_ENG_value = 0
        self.student_type = 0
        self.major = 0
        self.other_major = 0
        self.STEM_Classes = 0
        self.College = 0
        self.Other_College = 0
        self.high_school_partial = ''
        self.high_school_full = ''
        self.high_school_other = ''
        self.address1 = 0
        self.address2 = 0
        self.city = 0
        self.state = 0
        self.zip_code = 0
        self.address_type = ''
        self.home_latitude = 0
        self.home_longitude = 0
        self.home_to_school_dist = 0
        self.home_to_school_time_pt = 0  # public transit
        self.home_to_school_time_car = 0  # car

        # Score fields
        self.GPA_Score = 0
        self.ACT_SAT_Score = 0
        self.ACTM_SATM_Score = 0
        self.reviewer_score = 0

        # Validation Errors
        self.ChicagoResident = False
        self.ChicagoSchool = False
        self.school_found = False
        self.accredited = False
        self.valid_major = False
        self.past_recipient = False
        self.ACT_SAT_conversion = False
        self.ACT_SAT_decimal = False
        self.ACT_SAT_low = False
        self.ACT_SAT_high = False
