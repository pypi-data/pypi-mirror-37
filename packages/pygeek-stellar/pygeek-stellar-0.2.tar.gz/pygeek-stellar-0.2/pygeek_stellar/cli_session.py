# 3rd party imports
from stellar_base.keypair import Keypair
# Local imports
from .constants import *
from .utils.user_input import *
from .utils.file import *
from .utils.generic import *
from .utils.stellar import *


class CliSession:
    """
    
    Attributes
    ----------
    account_name : str
        Name of the Stellar account used on the CLI session.
    account_address : str
        Address of the Stellar account used on the CLI session.
    account_seed : str
        Secret seed of the Stellar account used on the CLI session. The seed
        is a string that can be used to decode both private and public key of the account.
    """

    def __init__(self, account_name, account_address, account_seed):

        self.account_name: str = account_name
        self.account_address: str = account_address
        self.account_seed: str = account_seed

    def store_account_in_config_file(self):
        if not _config_file_exists():
            password = password_input("Please insert an encryption/decryption password "
                                      "to protect the configuration file")
            if password != password_input("Please insert the encryption/decryption password again"):
                print("The inserted passwords are distinct. The configuration file could not be created")
                return
            configs_json = CONFIG_FILE_EMPTY_JSON
        else:
            password = password_input("Please insert the decryption password of the configuration file")
            configs_json = _config_file_load(password)
            if configs_json is None:
                print("The configuration file is either empty, could not be decrypted or is an invalid JSON file.")
                return

        configs_json[JSON_ACCOUNTS_TAG].append({
            JSON_ACCOUNT_NAME_TAG: self.account_name,
            JSON_ACCOUNT_ADDRESS_TAG: self.account_address,
            JSON_ACCOUNT_SEED_TAG: self.account_seed})

        _config_file_write(json.dumps(configs_json), password)

    def fetch_valid_seed(self):
        if self.account_seed is None \
                or not is_seed_valid(self.account_seed) \
                or not is_seed_matching_address(self.account_seed, self.account_address):
            self.account_seed = self.ask_for_user_seed("Either no seed was found for this CLI session account, "
                                                       "the seed for this CLI session account is invalid or "
                                                       "the seed does match the current CLI session account address. "
                                                       "No transaction can be made without a valid seed. Please "
                                                       "insert your seed to process the transaction")
        return self.account_seed

    def ask_for_user_seed(self, msg):
        seed = password_input(msg)
        if not is_seed_valid(seed):
            print('The given seed is invalid')
            return None

        if not is_seed_matching_address(seed, self.account_address):
            print('The given seed does not match with the address of the current CLI session')
            return None

        if yes_or_no_input('Do you want to save the seed for this CLI session account?') == USER_INPUT_YES:
            self.account_seed = seed

        return seed

    def to_str(self):
        return 'Account Name: {}, Account Address: {}'.format(self.account_name, self.account_address)


def init_cli_session():
    """
    This function initializes a CLI session. There are three alternatives to initialize a session:
    1: Initialize from an account stored on the configuration file.
    2: Initialize from an existent account which is not stored on the configuration file.
    3: Initialize from a newly created Stellar account.
    :return: Returns the initialized CLI session or None if something went wrong.
    :rtype: CliSession or None
    """
    if not _config_file_exists():
        print("No configuration file was found.")
    elif yes_or_no_input('Do you want to use an account from the configuration file?') == USER_INPUT_YES:
        return _init_session_from_conf_file()

    if yes_or_no_input('Do you want to use an existent account?') == USER_INPUT_YES:
        return _init_session_from_existent_account()

    if yes_or_no_input('Do you want to create a new account?') == USER_INPUT_YES:
        return _init_session_from_new_account()

    return None


def _init_session_from_conf_file():
    """
    Initializes a session from an account stored on the configuration file. This function assumes that the
    configuration file already exists. This method can fail in the following situations:
    1: The configuration file is empty.
    2: The configuration file could not be decrypted (for example if a wrong decryption password was given).
    3: The configuration file is not a valid JSON file.
    4: The configuration file does not have the 'accounts' JSON key, or there are no accounts stored on it.
    5: The index of the configuration file account specified by the user is invalid.
    :return: Returns the initialized CLI session or None if something went wrong.
    :rtype: CliSession or None
    """
    configs_json, conf_file_password = _config_file_load()
    if configs_json is None:
        print("The configuration file is either empty, could not be decrypted or is an invalid JSON file.")
        return None

    if not _config_file_is_valid_content(configs_json):
        print("The content of the configuration file is invalid")
        return None

    n_accounts_found = _config_file_get_number_of_accounts(configs_json)
    if n_accounts_found <= 0:
        print("No accounts were found on the configuration file.")
        return None

    _config_file_print_accounts(configs_json)
    account_n = int_input('Which account do you want to use? (specify the index)') - 1
    if account_n < 0 or account_n >= n_accounts_found:
        print("Specified account index is invalid")
        return None

    name = configs_json[JSON_ACCOUNTS_TAG][account_n][JSON_ACCOUNT_NAME_TAG]
    address = configs_json[JSON_ACCOUNTS_TAG][account_n][JSON_ACCOUNT_ADDRESS_TAG]
    seed = configs_json[JSON_ACCOUNTS_TAG][account_n].get(JSON_ACCOUNT_SEED_TAG, None)
    return CliSession(name, address, seed)


def _init_session_from_existent_account():
    """
    Initializes a session from an account which is not stored on the configuration file. This method fails
    if the given Stellar address is invalid.
    :return: Returns the initialized CLI session or None if something went wrong.
    :rtype: CliSession or None
    """
    address = safe_input("Please insert the address of the existent account")
    if not is_address_valid(address):
        print("The specified address is not a valid Stellar address.")
        return None

    cli_session = CliSession(None, address, None)
    if _config_file_is_to_update():
        if yes_or_no_input("Do you want to give a name to the new account to be created?") == USER_INPUT_YES:
            cli_session.account_name = safe_input("Please insert the account name")
        cli_session.store_account_in_config_file()
    return cli_session


def _init_session_from_new_account():
    """
    Initializes a session from a newly created account. A Stellar keypair is randomly generated.
    :return: Returns the initialized CLI session.
    :rtype: CliSession
    """
    account_name = None
    if yes_or_no_input("Do you want to give a name to the new account to be created?") == USER_INPUT_YES:
        account_name = safe_input("Please insert the account name")

    keypair = Keypair.random()
    address = keypair.address().decode()
    seed = keypair.seed().decode()

    cli_session = CliSession(account_name, address, seed)
    if _config_file_is_to_update():
        if yes_or_no_input("Do you want to save the seed of the new account in the encrypted configuration file") == \
                USER_INPUT_YES:
            cli_session.store_account_in_config_file()
        else:
            seed_file = safe_input("Specify a file to which the seed of the new created account should be saved. "
                                   "Notice that the seed will be saved in plain text on the specified file. "
                                   "Please store it in a safe place. If anyone can reach the seed it can fully "
                                   "control your account")
            write_file(seed_file, seed)
            cli_session.store_account_in_config_file()
    return cli_session


def _config_file_print_accounts(configs_json):
    """
    Prints the accounts found on the configuration file.
    :param json configs_json: Configuration file JSON decoded data.
    """
    accounts = _config_file_get_accounts(configs_json)
    print('The following {} Stellar accounts were found on the configuration file:'.format(len(accounts)))
    for i, account in enumerate(accounts):
        print('[{}] Account Name: {}, Account Address: {}'.format(
            i+1, account[JSON_ACCOUNT_NAME_TAG], account[JSON_ACCOUNT_ADDRESS_TAG]))
    print('')


def _config_file_exists():
    """
    Checks if the configuration file exists.
    :return: Returns True if the configuration file exists and False otherwise.
    :rtype: bool
    """
    if os.path.isfile(DEFAULT_CONFIG_FILE):
        return True
    return False


def _config_file_load(password=None):
    """
    Requests a password to decrypt the configuration file, decrypts it and returns the decoded JSON content
    together with the decryption password. If the file cannot be opened or decrypted or if its content cannot
    be decoded as JSON this method returns None.
    :param str password: Password to decrypt the file. If no password is given one is requested from the user.
    :return: In case of success it returns.
    :rtype: (json, str) or (None, None)
    """
    if password is None:
        password = password_input("Please insert the configuration file decryption password")
    configs_content = decode_json_content(load_encrypted_file(DEFAULT_CONFIG_FILE, password))
    return (None, None) if configs_content is None else (configs_content, password)


def _config_file_write(config_json, password):
    """
    Encrypts the specified content with the given password and writes it to the configuration file.
    :param json config_json: Content to be stored on the configuration file.
    :param password: Encryption password,
    """
    file = DEFAULT_CONFIG_FILE
    succeeded = write_encrypted_file(file, config_json, password)
    if succeeded:
        print("Configuration file successfully stored in: {}".format(file))


def _config_file_is_to_update():
    """
    Ask the user if the configuration file should be updated or not.
    :return: Returns True if the user wants to update the configuration file and False otherwise.
    :rtype: bool
    """
    if yes_or_no_input("Do you want to save the account on the configuration file?") == USER_INPUT_YES:
        return True
    return False


def _config_file_is_valid_content(configs_json):
    """
    Checks if the content of the configuration file is valid. For this to be true an 'accounts' JSON key
    must be found.
    :param json configs_json: Configuration file JSON decoded data.
    :return: Returns True if the content is valid and False otherwise.
    :rtype: bool
    """
    if JSON_ACCOUNTS_TAG in configs_json:
        return True
    return False


def _config_file_get_number_of_accounts(configs_json):
    """
    Returns the number of accounts stored on the configuration file.
    :param json configs_json: Configuration file JSON decoded data.
    :return: Returns the number of accounts stored on the configuration file.
    :rtype: int
    """
    return len(configs_json[JSON_ACCOUNTS_TAG])


def _config_file_get_accounts(configs_json):
    """
    Returns the accounts stored on the configuration file. It assumes that the given configuration JSON
    content is valid (which means that it must have an 'accounts' JSON key).
    :param json configs_json: Configuration file JSON decoded data.
    :return: Returns the accounts stored on the configuration file.
    :rtype: json
    """
    return configs_json[JSON_ACCOUNTS_TAG]
