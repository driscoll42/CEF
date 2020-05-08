class Student:
    """A student class to track values and validation failures"""

    def __init__(self, firstName, lastName):
        self.lastName = lastName
        self.firstName = firstName
        self.GPA_Value = 0.0
        self.ACT_SAT_value = 0.0
        self.ACTM_SATM_value = 0.0
        self.COMMS_value = 0.0
        self.NON_ENG_value = ''
        self.student_type = ''
        self.major = ''
        self.other_major = ''
        self.STEM_Classes = ''
        self.College = ''
        self.Other_College = ''
        self.high_school_partial = ''
        self.high_school_full = ''
        self.high_school_other = ''
        self.address1 = ''
        self.address2 = ''
        self.city = ''
        self.state = ''
        self.zip_code = ''
        self.cleaned_address1 = ''
        self.cleaned_address2 = ''
        self.cleaned_city = ''
        self.cleaned_state = ''
        self.cleaned_zip_code = ''
        self.address_footnotes = ''
        self.address_type = ''
        self.submitted = ''
        self.home_latitude = 0
        self.home_longitude = 0
        self.home_to_school_dist = 0.0
        self.home_to_school_time_pt = 0.0  # public transit
        self.home_to_school_time_car = 0.0  # car

        # Score fields
        self.GPA_Score = 0.0
        self.ACT_SAT_Score = 0.0
        self.ACTM_SATM_Score = 0.0
        self.STEM_Score = 0.0
        self.reviewer_score = 0.0

        # Validation Errors
        self.validationError = False
        self.valid_address = True
        self.ChicagoHome = True
        self.ChicagoSchool = True
        self.school_found = True
        self.distance_warn = True
        self.accredited = True
        self.valid_major = True
        self.past_recipient = True
        self.ACT_SAT_conversion = True
        self.ACT_SAT_decimal = True
        self.ACT_SAT_low = True
        self.ACT_SAT_high = True
        self.GPA_C_Under = True
        self.GPA_C_Warn = True
        self.C_Major_Warn = True
        self.C_College_change = True
        self.other_error = True
        self.other_error_message = ''
