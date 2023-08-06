# System imports
import getpass
# Local imports
from .generic import *

USER_INPUT_YES = 'y'
USER_INPUT_NO = 'n'


def int_input(msg):
    """
    This methods should be used to request an integer value from the user. This
    method will not return until the user inputs a valid integer value.
    :param str msg: Message to be displayed to the user.
    :return: Returns the integer value inserted by the user.
    :rtype: int
    """
    value = safe_input(msg)
    while not is_int_str(value):
        print('Input must be a valid integer value')
        value = safe_input(msg)
    return int(value, base=10)


def float_input(msg):
    """
    This methods should be used to request a float value from the user. This
    method will not return until the user inputs a valid float value.
    :param str msg: Message to be displayed to the user.
    :return: Returns the float value inserted by the user.
    :rtype: float
    """
    value = safe_input(msg).replace(',', '.')
    while not is_float_str(value):
        print('Input must be a valid float value')
        value = safe_input(msg).replace(',', '.')
    return float(value)


def yes_or_no_input(msg):
    """
    This methods should be used to request an Yes/No input from the user. This
    method will not return until the user inputs a valid answer (USER_INPUT_YES or
    USER_INPUT_NO).
    :param str msg: Message to be displayed to the user.
    :return: Returns USER_INPUT_YES if the answer is affirmative and USER_INPUT_NO otherwise.
    :rtype: str
    """
    full_msg = '{} ({}/{})'.format(msg, USER_INPUT_YES, USER_INPUT_NO)
    answer = safe_input(full_msg).lower()
    while answer not in [USER_INPUT_YES, USER_INPUT_NO]:
        answer = safe_input(full_msg).lower()
    return answer


def password_input(msg):
    """
    This methods should be used to request a password input from the user. With
    this method the password inserted by the user will not be displayed on the
    screen. It also exits gracefully in case of a KeyboardInterrupt signal (ctr+c)
    being received.
    :param str msg: Message to be displayed to the user.
    :return: Returns the password inserted by the user.
    :rtype: str
    """
    try:
        return getpass.getpass('{}: '.format(msg))
    except KeyboardInterrupt:
        print('\n\nExiting..')
        raise SystemExit


def safe_input(msg):
    """
    This method extends the system built input() method in order to exit gracefully
    in case of a KeyboardInterrupt signal (ctr+c) being received.
    :param str msg: Message to be displayed to the user.
    :return: Returns the input inserted by the user.
    :rtype: str
    """
    try:
        return input('{}: '.format(msg))
    except KeyboardInterrupt:
        print('\n\nExiting..')
        raise SystemExit
