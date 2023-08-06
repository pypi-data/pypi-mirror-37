# 3rd party imports
# Local imports
from .utils.stellar import *


def get_account_balances(account_address):
    """
    This method is used to fetch all the balances from the given account address.
    :param str account_address: Account address to be evaluated.
    :return: Returns a list containing the account balances structured in the following manner
    : [['token1', amount], ['token2', amount]]
    :rtype: list of (str, str)
    """
    address = get_address_details_from_network(account_address)
    if address is None:
        return None

    balances = []
    for balance in address.balances:
        token_code = balance.get('asset_code', 'XLM')
        token_balance = float(balance.get('balance'))
        balances.append([token_code, token_balance])
    return balances


def get_account_payments(account_address):
    """
    This method is used to fetch all the payments from the given account address.
    :param str account_address: Account address to be evaluated.
    :return: Returns a JSON string with the payments. TODO: The string must be parsed
    :rtype: str
    """
    address = get_address_details_from_network(account_address)
    if address is None:
        return None

    return address.payments()


def get_account_transactions(account_address):
    """
    This method is used to fetch all the transactions from the given account address.
    :param str account_address: Account address to be evaluated.
    :return: Returns a JSON string with the transactions. TODO: The string must be parsed
    :rtype: str
    """
    address = get_address_details_from_network(account_address)
    if address is None:
        return None

    return address.transactions()
