# System imports
import os
# Local imports
from .cryptography import *

FILE_MODE_READ = 'r'
FILE_MODE_READ_BINARY = 'rb'
FILE_MODE_WRITE = 'w'
FILE_MODE_WRITE_BINARY = 'wb'


def write_file(filename, content, write_as_binary=False):
    """
    Writes the given content to the specified file.
    :param str filename: File to which the content should be written.
    :param str content: Content to be written.
    :param bool write_as_binary: Flag that specifies if the content must be written in binary form or not.
    This parameter is optional and by default files are not written is binary form.
    :return: Returns True in case of success and false otherwise.
    :rtype: bool
    """
    opening_mode = FILE_MODE_WRITE if not write_as_binary else FILE_MODE_WRITE_BINARY
    try:
        file = open(filename, opening_mode)
        file.write(content)
        file.close()
        return True
    except (OSError, IOError):
        print("There was a problem opening/writing the file: {}".format(filename))
        return False


def load_file(filename, read_as_binary=False):
    """
    Loads the specified file to memory.
    :param str filename: File to be loaded.
    :param bool read_as_binary: Flag that specifies if the file must be loaded in binary form or not.
    This parameter is optional and by default files are not loaded is binary form.
    :return: Returns the content of the file or None if the file could not be read.
    :rtype: str or bytearray or None
    """
    if os.path.isfile(filename):
        opening_mode = FILE_MODE_READ if not read_as_binary else FILE_MODE_READ_BINARY
        try:
            with open(filename, opening_mode) as file_content:
                return file_content.read()
        except (OSError, IOError):
            print("There was a problem opening/reading the file: {}".format(filename))
            return None
    return None


def write_encrypted_file(filename, content, password):
    """
    Writes the given content to the specified file and encrypts it with the specified password.
    :param str filename: File to which the content should be written.
    :param str content: Content to be written.
    :param str password: Password to encrypt the file.
    :return: Returns True in case of success and false otherwise.
    :rtype: bool
    """
    if not _is_valid_password(password):
        print('A valid password must be given to decrypt the file')
        return False

    encrypted_content = encrypt(content.encode(), password)
    return write_file(filename, encrypted_content, write_as_binary=True)  # Encrypted files are stored as binary


def load_encrypted_file(filename, password, read_as_binary=False):
    """
    Loads the specified file to memory and decrypts it with the specified password.
    :param str filename: File to be loaded.
    :param str password: Password to decrypt the file.
    :param bool read_as_binary: Flag that specifies if the file must be loaded in binary form or not.
    This parameter is optional and by default files are not loaded is binary form.
    :return: Returns the content of the file or None if the file could not be read.
    :rtype: str or bytearray or None
    """
    if not _is_valid_password(password):
        print('A valid password must be given to decrypt the file')
        return None

    file_content = load_file(filename, read_as_binary=True)  # Encrypted files are stored as binary
    if file_content is None:
        return None

    decrypted_content = decrypt(file_content, password)
    if decrypted_content is None:
        return None

    return decrypted_content if read_as_binary else decrypted_content.decode()


def _is_valid_password(password):
    """
    Evaluates if a given password is valid. Its length must be higher than 0.
    :param str password: Password to be evaluated.
    :return: Returns True if the password is valid and False otherwise.
    :rtype: bool
    """
    if password is None or len(password) == 0:
        return False
    return True
