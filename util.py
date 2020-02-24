import csv
import re


# Too much of the data is dirty often times, this function gets the first number in a string, and returns it
# If there is no number, or it's NULL, it returns a 0
def get_num(input_text: str) -> float:
    """Returns the first number in a string."""

    list_of_nums = re.findall(r'\d+', input_text)
    if len(list_of_nums) == 0:
        return 0.0
    else:
        return float(list_of_nums[0])


def conversion_dict(file_name: str) -> dict:
    # This function assumes your from value is in the first column of the csv and your to is in the second
    # Further it assumes the first column has not repeats
    # Also assumes that all the values in the table are integers
    with open('Conversions/' + str(file_name), 'r', encoding="utf-8-sig") as f:
        d_reader = csv.DictReader(f)

        # get fieldnames from DictReader object and store in list
        headers = d_reader.fieldnames
        conv_doc = {}
        header_one = headers[0]
        header_two = headers[1]

        for line in d_reader:
            conv_doc[int(line[header_one])] = int(line[header_two])

    return conv_doc
