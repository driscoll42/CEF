def unit_tests(student_list: list, CALL_APIS: bool = False):
    for s in student_list:

        if s.lastName == 'HSValidation':
            if s.firstName == 'Pass':
                assert (s.validationError is False), "HS Pass failed"
            # elif s.firstName == 'CHomeNoCSchool': There's no need to test this as we only check the school's city if the home isn't Chicago
            #    assert (s.ChicagoSchool is False), "HS CHomeNoCSchool failed"
            elif s.firstName == 'NotAResidence' and CALL_APIS:
                assert (s.valid_address is False), "HS NotAResidence failed"
            elif s.firstName == 'NotAccredCollege':
                assert (s.accredited is False), "NotAccredCollege failed"
            elif s.firstName == 'NotAccredMajor':
                assert (s.accredited is False), "HS NotAccredMajor failed"
            elif s.firstName == 'AccredCollegeUndecided':
                assert (s.accredited is True), "HS AccredCollegeUndecided failed"
            elif s.firstName == 'NoCSchoolOrHome':
                assert (s.ChicagoSchool is False), "HS NoCSchoolOrHome ChicagoSchool failed"
                assert (s.ChicagoHome is False), "HS NoCSchoolOrHome ChicagoHome failed"
            elif s.firstName == 'ChicagoSchoolNoCHome':
                assert (s.ChicagoHome is False), "HS ChicagoSchoolNoCHome failed"

        if s.lastName == 'CValidation':
            if s.firstName == 'Pass':
                assert (s.validationError is False), "C Pass failed"
            elif s.firstName == 'NotPastRecipient':
                assert (s.past_recipient is False), "C NotPastRecipient failed"
            elif s.firstName == 'GPAFail':
                assert (s.GPA_C_Under is False), "C GPAFail failed"
            elif s.firstName == 'GPAWarn':
                assert (s.GPA_C_Warn is False), "C GPAWarn failed"
            elif s.firstName == 'InvalidMajor':
                assert (s.C_Major_Warn is False), "C InvalidMajor failed"
