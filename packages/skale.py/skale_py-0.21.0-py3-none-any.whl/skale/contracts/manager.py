from web3 import Web3
import socket
import logging

from skale.contracts import BaseContract
import skale.utils.helper as Helper
from skale.utils.helper import sign_and_send

from skale.utils.constants import NODE_DEPOSIT, GAS, OP_TYPES

logger = logging.getLogger(__name__)


class Manager(BaseContract):

    def create_node(self, ip, port, name, wallet):
        logger.info(f'create_node: {ip}:{port}, name: {name}')

        token = self.skale.get_contract_by_name('token')
        skale_nonce = Helper.generate_nonce()
        transaction_data = self.create_node_data_to_bytes(ip, port, name, wallet['address'], skale_nonce)

        op = token.contract.functions.transfer(self.address, NODE_DEPOSIT, transaction_data)
        tx = sign_and_send(self.skale, op, GAS['create_node'], wallet)
        return {'tx': tx, 'nonce': skale_nonce}

    def create_node_data_to_bytes(self, ip, port, name, address, nonce):
        address_fx = Web3.toChecksumAddress(address)[2:]  # fix & cut 0x

        type_bytes = OP_TYPES['create_node'].to_bytes(1, byteorder='big')
        port_bytes = port.to_bytes(4, byteorder='big')
        nonce_bytes = nonce.to_bytes(4, byteorder='big')  # todo
        ip_bytes = socket.inet_aton(ip)
        address_bytes = bytes.fromhex(address_fx)
        name_bytes = name.encode()

        data_bytes = type_bytes + port_bytes + nonce_bytes + ip_bytes + address_bytes + name_bytes
        logger.info(f'create_node_data_to_bytes bytes: {self.skale.web3.toHex(data_bytes)}')

        return data_bytes

    def create_schain(self, storage_bytes, cpu, transaction_throughput, lifetime, type_of_nodes, deposit, name, wallet):
        logger.info(f'create_schain: type_of_nodes: {type_of_nodes}, name: {name}')

        token = self.skale.get_contract_by_name('token')
        skale_nonce = Helper.generate_nonce()
        transaction_data = self.create_schain_data_to_bytes(storage_bytes, cpu, transaction_throughput, lifetime,
                                                            type_of_nodes, name, skale_nonce)

        op = token.contract.functions.transfer(self.address, deposit, transaction_data)
        tx = sign_and_send(self.skale, op, GAS['create_node'], wallet)
        return {'tx': tx, 'nonce': skale_nonce}

    def create_schain_data_to_bytes(self, storage_bytes, cpu, transaction_throughput, lifetime, type_of_nodes,
                                    name, nonce):
        type_bytes = OP_TYPES['create_schain'].to_bytes(1, byteorder='big')
        storage_bytes_hex = storage_bytes.to_bytes(32, byteorder='big')
        cpu_hex = cpu.to_bytes(32, byteorder='big')
        transaction_throughput_hex = transaction_throughput.to_bytes(32, byteorder='big')
        lifetime_hex = lifetime.to_bytes(32, byteorder='big')
        type_of_nodes_hex = type_of_nodes.to_bytes(1, byteorder='big')
        nonce_hex = nonce.to_bytes(2, byteorder='big')
        name_hex = name.encode()

        data_bytes = type_bytes + storage_bytes_hex + cpu_hex + transaction_throughput_hex + lifetime_hex + type_of_nodes_hex + nonce_hex + name_hex
        logger.info(f'create_schain_data_to_bytes bytes: {self.skale.web3.toHex(data_bytes)}')
        return data_bytes

    def get_bounty(self, node_id, wallet):
        op = self.contract.functions.getBounty(node_id)
        tx = sign_and_send(self.skale, op, GAS['get_bounty'], wallet)
        return {'tx': tx}

    def send_verdict(self, validator, node_id, downtime, latency, wallet):
        op = self.contract.functions.sendVerdict(validator, node_id, downtime, latency)
        tx = sign_and_send(self.skale, op, GAS['send_verdict'], wallet)
        return {'tx': tx}

    def get_node_next_reward_date(self, node_index):
        return self.contract.functions.getNodeNextRewardDate(node_index).call()
