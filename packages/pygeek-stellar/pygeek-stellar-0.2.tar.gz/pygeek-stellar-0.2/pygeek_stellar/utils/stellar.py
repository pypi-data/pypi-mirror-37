# 3rd party imports
import stellar_base.utils
from stellar_base.exceptions import *
from stellar_base.keypair import Keypair
from stellar_base.address import Address

STELLAR_MEMO_TEXT_MAX_BYTES = 28


def is_address_valid(address):
    """
    Checks if a given Stellar address is valid. It does not check if it exists on the Stellar
    network, only if it is correctly formatted.
    :param str address: address to be evaluated.
    :return: Returns true if the given address is valid and false otherwise.
    :rtype: bool
    """
    if address is None:
        return False
    try:
        stellar_base.utils.decode_check('account', address)
        return True
    except DecodeError:
        return False


def is_seed_valid(key):
    """
    Checks if a given Stellar seed is valid.
    :param str key: Seed to be evaluated.
    :return: Returns true if the seed is valid and false otherwise.
    :rtype: bool
    """
    if key is None:
        return False
    try:
        stellar_base.utils.decode_check('seed', key)
        return True
    except DecodeError:
        return False


def is_transaction_text_memo_valid(memo):
    """
    Checks if a given Stellar transaction text memo is valid. To be valid the text memo
    can only have, at most, 28 bytes.
    :param str memo: Text memo to be evaluated.
    :return: Returns true if the given text memo is valid and false otherwise.
    :rtype: bool
    """
    if memo is None:
        return False
    return False if len(memo) > STELLAR_MEMO_TEXT_MAX_BYTES else True


def is_seed_matching_address(seed, address):
    """
    Checks if the specified seed address matches the specified address.
    :param str seed: Seed to be evaluated.
    :param str address: Address to be evaluated.
    :return: Returns true if seed address matches the specified address, and false otherwise.
    :rtype: bool
    """
    if not is_seed_valid(seed) \
            or not is_address_valid(address):
        return False

    keypair = Keypair.from_seed(seed=seed)
    if keypair.address().decode() == address:
        return True
    return False


def is_account_existent(address):
    """
    Checks if a given Stellar address exists in the network. It assumes that the address
    parameter received is a valid address string.
    :param str address: address to be evaluated.
    :return: Returns true if the given address exists in the network and false otherwise.
    :rtype: bool
    """
    return True if get_address_details_from_network(address) is not None else False


def get_address_details_from_network(address):
    """
    Queries the Stellar network regarding the details of the specified account address.
    :param str address: address to be evaluated.
    :return: In case of success returns a Stellar Address object with the updated address information, fetched from
    the Stellar network. In case of failure returns None
    :rtype: Address or None
    """
    if not is_address_valid(address):
        print('Trying to get information of an invalid address.')
        return None

    try:
        address = Address(address=address)
        address.get()  # Get the latest information from Horizon
    except AccountNotExistError:
        print('The specified account does not exist.')
        return None
    except HorizonError:
        print('A connection error occurred (Please check your Internet connection).')
        return None
    return address
