import csv
from typing import Tuple

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

import constants as cs
from utils import keys as keys


# Source: https://smartystreets.com/docs/sdk/python
def address_validation(lastName: str, firstName: str, address1: str, address2: str, city: str, state: str,
                       zip_code: str) -> Tuple[str, float, float]:
    """This function will check a given address to determine what type of address it is, either residential, commercial,
        or if it is invalid. If the address is valid, it will also return the longitude and latitude of the address

    Parameters
    ----------
    lastName : str
        Applicant's last name
    firstName : str
        Applicant's first name
    address1 : str
        Applicant's home address line 1
    address2 : str
        Applicant's home address line 2
    city : str
        Applicant's home city
    state : str
        Applicant's home state
    zip_code : str
        Applicant's home zip_code

    Returns
    -------
    residency : str
        'Residential', 'Commercial', or 'Invalid Address' based on the USPS database
    latitude : float
        The latitude of the address given
    longitude : float
        The longitude of the address given

    """
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
    lookup.zipcode = zip_code
    lookup.candidates = 3
    lookup.match = "strict"  # "invalid" is the most permissive match,
    # this will always return at least one result even if the address is invalid.
    # Refer to the documentation for additional Match Strategy options.
    # This has been modified to strict to only get valid addresses

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return 'Error', 0.0, 0.0

    result = lookup.result

    if not result:
        # print("No candidates. This means the address is not valid.")
        return 'Invalid Address', 0.0, 0.0

    first_candidate = result[0]

    residency = first_candidate.metadata.rdi
    latitude = first_candidate.metadata.latitude
    longitude = first_candidate.metadata.longitude

    return residency, latitude, longitude


def accred_check(school_list: list, other_school: list, major: str) -> bool:
    """This function will determine if the applicant is going to an ABET accredited program. This requires that an
    extract from ABET's website in the "School_Data" folder. As an applicant can have multiple schools listed, this
    function iterates over all of them and checks if they are in the ABET list. If so it then compares the major the
    applicant is taking and sees if the program is accredited at that school. If the applicant's major is "Undecided
    Engineering", the function just checks that the school has ABET accredited engineering programs.


    Parameters
    ----------
    school_list : list
        The list of all the school's the applicant is accepted to from a predefined list setup on AwardSpring
    other_school : list
        The list of schools the applicant is accepted to from the free form field if the above is "Not Listed"
    major : str
        A string containing the majors the applicatn is applying for

    Returns
    -------
    accredited : bool
        A bool if the school and major combination is accredited or not

    """
    accredited = False

    major = major.upper()
    major = major.strip()
    major = major.replace(' AND ', ',')
    major = major.replace(' ', '')
    major = major.replace('ENGINEERING', '')
    major_list = major.split(',')

    for school in school_list:
        school = school.upper()
        school = school.strip()
        school = school.replace('THE ', '')
        school = school.replace(' AT ', ' - ')
        school = school.replace('-', '')
        school = school.replace(' ', '')

        with open('School_Data/ABET_Accredited_Schools.csv', 'r', encoding="utf-8-sig") as f:
            d_reader = csv.DictReader(f)
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

    return accredited


def get_past_recipients(file: str) -> list:
    """ A simple function to turn a file containing the list of past recipients of the award into a list

    Parameters
    ----------
    file : str
        A csv containing a list of past recipients

    Returns
    -------
    recipient_list: list
        A list with all the names of the past recipients
    """
    recipient_list = []

    with open('Student_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        # get fieldnames from DictReader object and store in list
        d_reader = csv.DictReader(f)
        for line in d_reader:
            lastName = line[cs.questions['lastName']]
            firstName = line[cs.questions['firstName']]
            recipient_list.append(lastName.strip().upper() + firstName.strip().upper())
    return recipient_list


def get_school_list(file: str) -> dict:
    """ A simple function to turn a file containing the list of high schools in Illinois with their cityand return it
        as a dict

    Parameters
    ----------
    file : str
        A csv containing a list of high school/city combinations

    Returns
    -------
    school_list: dict
        A dictionary with a key of high school name and a value of the city the school is in
    """
    school_list = {}
    with open('School_Data/' + str(file), 'r', encoding="utf-8-sig") as f:
        d_reader = csv.DictReader(f)
        for line in d_reader:
            school_list[line['FacilityName'].upper()] = line['City'].upper()

    return school_list
