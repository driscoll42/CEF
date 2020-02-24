import csv

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

import constants as cs
import keys as keys


# Source: https://smartystreets.com/docs/sdk/python
def address_Validation(lastName: str, firstName: str, address1: str, address2: str, city: str, state: str, zip: str,
                       country: str) -> str:
    # We recommend storing your secret keys in environment variables instead---it's safer!
    # auth_id = os.environ['SMARTY_AUTH_ID']
    # auth_token = os.environ['SMARTY_AUTH_TOKEN']

    credentials = StaticCredentials(keys.auth_id, keys.auth_token)

    client = ClientBuilder(credentials).build_us_street_api_client()
    # client = ClientBuilder(credentials).with_custom_header({'User-Agent': 'smartystreets (python@0.0.0)', 'Content-Type': 'application/json'}).build_us_street_api_client()
    # client = ClientBuilder(credentials).with_proxy('localhost:8080', 'user', 'password').build_us_street_api_client()
    # Uncomment the line above to try it with a proxy instead

    # Documentation for input fields can be found at:
    # https://smartystreets.com/docs/us-street-api#input-fields

    lookup = StreetLookup()
    lookup.input_id = ""  # Optional ID from your system
    lookup.addressee = firstName + " " + lastName
    lookup.street = address1
    lookup.street2 = ""
    lookup.secondary = address2
    lookup.urbanization = ""  # Only applies to Puerto Rico addresses
    lookup.city = city
    lookup.state = state
    lookup.zipcode = zip
    lookup.candidates = 3
    lookup.match = "Invalid"  # "invalid" is the most permissive match,
    # this will always return at least one result even if the address is invalid.
    # Refer to the documentation for additional Match Strategy options.

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result

    if not result:
        # print("No candidates. This means the address is not valid.")
        return 'Invalid Address'

    first_candidate = result[0]

    return first_candidate.metadata.rdi


def accred_check(school_list: list, other_school: list, major: str) -> bool:
    major = major.upper()
    major = major.strip()
    major = major.replace(' AND ', ',')
    major = major.replace(' ', '')
    major = major.replace('ENGINEERING', '')
    major_list = major.split(',')
    Accredited = False

    for school in school_list:
        school = school.upper()
        school = school.strip()
        school = school.replace('THE ', '')
        school = school.replace(' AT ', ' - ')
        school = school.replace('-', '')
        school = school.replace(' ', '')

        with open('School_Data/ABET_Accredited_Schools.csv', 'r', encoding="utf-8-sig") as f:
            d_reader = csv.DictReader(f)
            headers = d_reader.fieldnames
            for line in d_reader:
                ABET_major = line[cs.abet_major]
                ABET_major = ABET_major.upper()
                ABET_major = ABET_major.strip()
                ABET_major = ABET_major.replace(' AND ', ',')
                ABET_major = ABET_major.replace(' ', '')
                ABET_major = ABET_major.replace('ENGINEERING', '')

                ABET_school = line[cs.abet_school_name]
                ABET_school = ABET_school.upper()
                ABET_school = ABET_school.strip()
                ABET_school = ABET_school.replace('THE ', '')
                ABET_school = ABET_school.replace(' AT ', ' - ')
                ABET_school = ABET_school.replace('-', '')
                ABET_school = ABET_school.replace(' ', '')
                if school in ABET_school:
                    for option in major_list:
                        if option == ABET_major or option == 'UNDECIDED' or option == '':
                            return True

    for school in other_school:
        school = school.upper()
        school = school.strip()
        school = school.replace('THE ', '')
        school = school.replace(' AT ', ' - ')
        school = school.replace('-', '')
        school = school.replace(' ', '')

        with open('School_Data/ABET_Accredited_Schools.csv', 'r', encoding="utf-8-sig") as f:
            d_reader = csv.DictReader(f)
            headers = d_reader.fieldnames
            for line in d_reader:
                ABET_major = line[cs.abet_major]
                ABET_major = ABET_major.upper()
                ABET_major = ABET_major.strip()
                ABET_major = ABET_major.replace(' AND ', ',')
                ABET_major = ABET_major.replace(' ', '')
                ABET_major = ABET_major.replace('ENGINEERING', '')

                ABET_school = line[cs.abet_school_name]
                ABET_school = ABET_school.upper()
                ABET_school = ABET_school.strip()
                ABET_school = ABET_school.replace('THE ', '')
                ABET_school = ABET_school.replace(' AT ', ' - ')
                ABET_school = ABET_school.replace('-', '')
                ABET_school = ABET_school.replace(' ', '')
                if school in ABET_school:
                    for option in major_list:
                        if option == ABET_major or option == 'UNDECIDED' or option == '':
                            return True

    return Accredited


def get_past_recipients(file: str) -> list:
    recipient_list = []

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]
            recipient_list.append(lastName.strip().upper() + firstName.strip().upper())
    return recipient_list


def get_school_list(file: str) -> list:
    school_list = {}
    with open('School_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        d_reader = csv.DictReader(f)
        for line in d_reader:
            school_list[line['FacilityName'].upper()] = line['City'].upper()

    return school_list
