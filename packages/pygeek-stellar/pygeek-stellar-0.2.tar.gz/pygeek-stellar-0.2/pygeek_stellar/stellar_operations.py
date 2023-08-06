# 3rd party imports
from stellar_base.operation import *


def create_account_creation_op(destination, starting_balance, source=None):
        """
        This method creates a Stellar account creation operation. This operation can be used
        to create a new Stellar account by transferring a certain amount of funds to it.
        :param str destination: Address of the new account to be created.
        :param str starting_balance: Amount of funds to transfer to the new account.
        :param str source: TODO
        :return: Returns the newly created operation.
        :rtype: CreateAccount
        """
        return CreateAccount(opts={
            'source': source,
            'destination': destination,
            'starting_balance': starting_balance
        })


def create_payment_op(destination, amount, asset_code='XLM', asset_issuer=None, source=None):
    """
    This method creates a Stellar payment operation. This operation can be used
    to transfer funds between two accounts.
    :param str destination: Destination address to which the funds must be sent.
    :param str amount: Amount of funds to transfer.
    :param str asset_code: Code of the asset to be transferred. If none is specified the native asset is chosen.
    :param str asset_issuer: Issuer of the asset.
    :param str source: TODO
    :return: Returns the newly created operation.
    :rtype: Payment
    """
    return Payment(opts={
        'source': source,
        'destination': destination,
        'asset': Asset(asset_code, asset_issuer),
        'amount': amount
    })


def create_path_payment_op(destination, send_code, send_issuer, send_max, dest_code,
                           dest_issuer, dest_amount, path, source=None):
        """
        This method creates a Stellar path payment operation. This operation can be used
        to use the Stellar decentralized exchange (SDEX) to automatically convert the sent
        asset to the destination asset using the specified path. This enable, for example,
        the source account to transfer XLM while the destination account receives €.
        :param str destination:
        :param str send_code:
        :param str send_issuer:
        :param str send_max:
        :param str dest_code:
        :param str dest_issuer:
        :param str dest_amount:
        :param path: TODO
        :param source: TODO
        :return: Returns the newly created operation.
        :rtype: PathPayment
        """
        assets = []
        for p in path:
            assets.append(Asset(p[0], p[1]))

        opts = {
            'source': source,
            'destination': destination,
            'send_asset': Asset(send_code, send_issuer),
            'send_max': send_max,
            'dest_asset': Asset(dest_code, dest_issuer),
            'dest_amount': dest_amount,
            'path': assets
        }
        return PathPayment(opts)


def create_trust_op(destination, code, limit=None, source=None):
    """
    This method creates a Stellar trust operation. This operation can be used
    to create, delete or update an existing trustline.
    :param str destination: Destination address to which the trustline refers.
    :param str code: Code of the asset to which the trustline refers.
    :param str limit: Amount limit of the asset for the trustline.
    :param str source: TODO
    :return: Returns the newly created operation.
    :rtype: ChangeTrust
    """
    return ChangeTrust(opts={
        'source': source,
        'asset': Asset(code, destination),
        'limit': limit
    })

