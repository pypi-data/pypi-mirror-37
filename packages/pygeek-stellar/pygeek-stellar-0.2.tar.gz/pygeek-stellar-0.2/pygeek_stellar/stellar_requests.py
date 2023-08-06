# System imports
import requests
import base64
# 3rd party imports
from stellar_base.operation import *
from stellar_base.builder import Builder
from stellar_base.stellarxdr import Xdr
from stellar_base.stellarxdr import StellarXDR_const
from xdrlib import Error as XDRError
# Local imports
from .utils.stellar import *
from .utils.user_input import *
from .constants import *
from .utils.generic import *
from .stellar_operations import *


def create_new_account(source_account_address, source_account_seed, new_account_address, amount, transaction_memo=''):
    """
    This method creates a new Stellar account. For this to be done a certain amount
    of XLM must be transferred from a source account to the new account.
    :param str source_account_address: Address of the account from which the funds to
    create the new account will be retrieved.
    :param str source_account_seed: Seed of the account from which the funds to
    create the new account will be retrieved.
    :param str new_account_address: Address of the new account.
    :param str amount: XLM amount to transfer to the new account.
    :param str transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    """
    if not is_seed_matching_address(source_account_seed, source_account_address):
        print("The new account could not be created. Either the given source account address or source"
              "account seed are invalid or they do not match.")
        return

    if not is_address_valid(new_account_address):
        print('The given account address is invalid')
        return

    if yes_or_no_input('To create the new account, a payment of {} XLM will be done '
                       'to the following address {}. Are you sure you want to proceed?'
                       .format(amount, new_account_address)) == USER_INPUT_NO:
        return

    op = create_account_creation_op(new_account_address, amount, source_account_address)
    response = submit_operations(source_account_seed, op, transaction_memo)
    # process_server_payment_response(response) # TODO: Parse response


def fund_using_friendbot(account_address):
    """
    This method is used to request the Stellar Friendbot to fund the given account
    address. This will only work on the Stellar testnet.
    :param str account_address: Account address to be funded.
    :return: Returns a string with the result of the fund request.
    :rtype: str
    """
    if not is_address_valid(account_address):
        return 'The given account address is invalid.'

    try:
        r = requests.get('{}/friendbot?addr={}'.format(STELLAR_HORIZON_TESTNET_URL, account_address))
        return 'Successful transaction request' if is_successful_http_status_code(r.status_code) \
            else 'Failed transaction request (Maybe this account was already funded by Friendbot). Status code {}'.\
            format(r.status_code)
    except requests.exceptions.ConnectionError:
        return "A connection error occurred (Please check your Internet connection)"


def send_payment(source_account_address, source_account_seed, destination_account_address,
                 token_code, amount, token_issuer=None, transaction_memo=''):
    """
    This method is used to send a transaction of the specified token to a given address.
    :param str source_account_address: Address of the account from which the funds will be sent.
    :param str source_account_seed: Seed of the account from which the funds will be sent.
    :param str destination_account_address: Destination address.
    :param str amount: Amount to be sent.
    :param str token_code: Code of the token to be sent.
    :param str token_issuer: Issuer of the token to be sent. It can be None when dealing with native asset (XLM).
    :param str transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    """
    if not is_seed_matching_address(source_account_seed, source_account_address):
        print("The payment could not be finalized. Either the given source account address or source"
              "account seed are invalid or they do not match.")
        return

    if not is_address_valid(destination_account_address):
        print('The given destination address is invalid')
        return
    if destination_account_address == source_account_address:
        print('Sending payment to own address. This is not allowed')
        return
    if token_issuer is not None and not is_address_valid(token_issuer):
        print('The given token issuer address is invalid')
        return
    if not is_transaction_text_memo_valid(transaction_memo):
        print('The maximum size of the text memo is {} bytes'.format(STELLAR_MEMO_TEXT_MAX_BYTES))
        return

    if yes_or_no_input('A payment of {} {} will be done to the following address {}. Are you sure you want to proceed?'
                       .format(amount, token_code, destination_account_address)) == USER_INPUT_NO:
        return

    operations = [create_payment_op(destination=destination_account_address,
                                    amount=amount,
                                    asset_code=token_code,
                                    asset_issuer=token_issuer,
                                    source=source_account_address)]
    response = submit_operations(source_account_seed, operations, transaction_memo)
    process_server_payment_response(response)


def send_path_payment(source_account_address, source_account_seed, destination_address,
                      code_token_to_send, max_amount_to_send, issuer_token_to_send,
                      code_token_to_be_received, amount_to_be_received, issuer_token_to_be_received,
                      payment_path, transaction_memo=''):
    if not is_seed_matching_address(source_account_seed, source_account_address):
        print("The path payment could not be finalized. Either the given source account address or source"
              "account seed are invalid or they do not match.")
        return

    if not is_address_valid(destination_address):
        print('The given destination address is invalid')
        return

    operations = [create_path_payment_op(destination_address,
                                         code_token_to_send, issuer_token_to_send, max_amount_to_send,
                                         code_token_to_be_received, issuer_token_to_be_received, amount_to_be_received,
                                         payment_path, source=source_account_address)]

    response = submit_operations(source_account_seed, operations, transaction_memo)
    # TODO: Deal with the response


def establish_trustline(source_account_address, source_account_seed, destination_account_address,
                        token_code, token_limit, transaction_memo=''):
    """
    This method is used to create a trustline for a given token code and up to the specified limit,
    with the specified destination account address.
    :param str source_account_address: Address of the account from which the funds will be sent.
    :param str source_account_seed: Seed of the account from which the funds will be sent.
    :param str destination_account_address: Destination address.
    :param str token_code: Code of the token to be sent.
    :param str token_limit: Token limit value of the trustline.
    :param str transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    """
    if not is_seed_matching_address(source_account_seed, source_account_address):
        print("The trustline could not be established. Either the given source account address or source"
              "account seed are invalid or they do not match.")
        return

    if not is_address_valid(destination_account_address):
        print('The given destination address is invalid')
        return
    if destination_account_address == source_account_address:
        print('Sending change of trust transaction to own address. This is not allowed')
        return
    if not is_transaction_text_memo_valid(transaction_memo):
        print('The maximum size of the text memo is {} bytes'.format(STELLAR_MEMO_TEXT_MAX_BYTES))
        return

    operations = [create_trust_op(destination_account_address,
                                  token_code,
                                  token_limit,
                                  source_account_address)]
    response = submit_operations(source_account_seed, operations, transaction_memo)
    #process_server_payment_response(response)


def submit_operations(account_seed, operations, transaction_memo):
    """
    This method signs the given operations and submits them to the Stellar network
    :param str account_seed: Seed of the account submitting the operations. It is required to sign the transactions.
    :param Operation operations: Operations to be submitted.
    :param str transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    :return: Returns a string containing the server response or None if the transaction could not be submitted.
    :rtype: str or None
    """
    try:
        builder = Builder(secret=account_seed)
    except Exception:
        # Too broad exception because no specific exception is being thrown by the stellar_base package.
        # TODO: This should be fixed in future versions
        print("An error occurred (Please check your Internet connection)")
        return None

    builder.add_text_memo(transaction_memo)
    for operation in operations:
        builder.append_op(operation)
    builder.sign()
    try:
        return builder.submit()
    except Exception:
        # Too broad exception because no specific exception is being thrown by the stellar_base package.
        # TODO: This should be fixed in future versions
        print("An error occurred (Please check your Internet connection)")
        return None


def process_server_payment_response(response):
    if response is None:
        return

    if response.get('status') is not None:
        print("Server response status code: {}".format(response.get('status')))
    if response.get('title') is not None:
        print("Server response title: {}".format(response.get('title')))
    if response.get('detail') is not None:
        print("Server response detail: {}".format(response.get('detail')))
    if 'extras' in response and 'result_xdr' in response['extras']:
        unpacked_tx_result = decode_xdr_transaction_result(response['extras']['result_xdr'])
        print_xdr_transaction_result(unpacked_tx_result)
    if 'result_xdr' in response:
        unpacked_tx_result = decode_xdr_transaction_result(response.get('result_xdr'))
        print_xdr_transaction_result(unpacked_tx_result)


def decode_xdr_transaction_result(xdr_string):
    try:
        xdr_bytes = base64.b64decode(xdr_string)
        return Xdr.StellarXDRUnpacker(xdr_bytes).unpack_TransactionResult()
    except TypeError or ValueError:
        print("Error during base64 decoding")
        return None
    except XDRError:
        print("Error during XDR unpacking procedure")
        return None


def print_xdr_transaction_result(unpacked_tx_result):
        payment_result = unpacked_tx_result.result.results[0].paymentResult
        print("Server response operation result: {}".format(
            'Succeeded' if unpacked_tx_result.result.code == StellarXDR_const.txSUCCESS else 'Failed'))
        print('Server response payment result: {} (Code: {})'.format(str(payment_result), payment_result.code))
