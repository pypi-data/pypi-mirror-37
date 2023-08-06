# System imports
import json
from json import JSONDecodeError


def is_float_str(string):
    """
    Checks if a given str can be successfully converted to a float value.
    :param str string: String to be evaluated.
    :return: Returns true if the string is float convertible and false otherwise.
    :rtype: bool
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_int_str(string):
    """
    Checks if a given str can be successfully converted to an integer value.
    :param str string: String to be evaluated.
    :return: Returns true if the string is integer convertible and false otherwise.
    :rtype: bool
    """
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_in_range(val, range_min, range_max):
    """
    Checks if the specified value is within the given range.
    :param (int, float) val: Value to be evaluated.
    :param (int, float) range_min: Range lower value.
    :param (int, float) range_max: Range higher value.
    :return: Returns true if the value is within the range and false otherwise.
    :rtype: bool
    """
    return True if range_min <= val <= range_max else False


def is_successful_http_status_code(status_code):
    """
    Checks if a given HTTP status code is successfull. For this to happen
    this value should be between 200 and 299 (2XX)
    :param int status_code: Status code to be evaluated.
    :return: Returns true if the status code is successful and false otherwise.
    :rtype: bool
    """
    return is_in_range(status_code, 200, 299)


def decode_json_content(content):
    """
    Decodes a given string content to a JSON object
    :param str content: content to be decoded to JSON.
    :return: A JSON object if the string could be successfully decoded and None otherwise
    :rtype: json or None
    """
    try:
        return json.loads(content) if content is not None else None
    except JSONDecodeError:
        print("The given content could not be decoded as a JSON file")
        return None
