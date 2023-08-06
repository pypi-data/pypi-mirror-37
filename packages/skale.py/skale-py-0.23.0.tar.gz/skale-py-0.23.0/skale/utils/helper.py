import json, socket, os
from random import randint
import ipaddress
from time import sleep
import logging

import string, random

logger = logging.getLogger(__name__)


def format(fields):
    """
        Transform array to object with passed fields
        Usage:
        @format(['field_name1', 'field_name2'])
        def my_method()
            return [0, 'Test']

        => {'field_name1': 0, 'field_name2': 'Test'}
    """

    def real_decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            obj = {}
            for i, field in enumerate(fields):
                obj[field] = result[i]
            return obj

        return wrapper

    return real_decorator


def get_receipt(web3, tx):
    return web3.eth.getTransactionReceipt(tx)


def get_eth_nonce(web3, address):
    return web3.eth.getTransactionCount(address)

def get_nonce(skale, address):
    lib_nonce = skale.nonces.get(address)
    if not lib_nonce:
        lib_nonce = get_eth_nonce(skale.web3, address)
        skale.nonces.get(address)
    else:
        lib_nonce += lib_nonce
    return lib_nonce

def sign_and_send(skale, method, gas_amount, wallet):
    eth_nonce = get_nonce(skale, wallet['address'])
    txn = method.buildTransaction({
        'gas': gas_amount,
        'nonce': eth_nonce
    })
    signed_txn = skale.web3.eth.account.signTransaction(txn, private_key=wallet['private_key'])
    tx = skale.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.info(f'{method.__class__.__name__} - transaction_hash: {skale.web3.toHex(tx)}')
    return tx


def await_receipt(web3, tx, retries=10, timeout=5):
    for _ in range(0, retries):
        receipt = get_receipt(web3, tx)
        if (receipt != None):
            return receipt
        sleep(timeout)
    return None


def ip_from_bytes(bytes):
    return socket.inet_ntoa(bytes)


def ip_to_bytes(ip):
    return socket.inet_aton(ip)


def check_port(port):
    if port not in range(1, 65535):
        raise ValueError(f'{port} does not appear to be a valid port. Allowed range: 1-65535')


def check_ip(ip):
    return ipaddress.ip_address(ip)


def generate_ws_addr(ip, port):
    check_ip(ip)
    check_port(port)
    return 'ws://' + ip + ':' + str(port)


def get_default_abipath():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    abi_dir = os.path.join(current_dir, os.pardir)
    return os.path.join(abi_dir, 'contracts_data.json')


def get_abi(abi_filepath=None):
    if not abi_filepath:
        abi_filepath = get_default_abipath()
    with open(abi_filepath) as data_file:
        data = json.load(data_file)
    return data


def generate_nonce():
    return randint(0, 65534)

def random_string(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))