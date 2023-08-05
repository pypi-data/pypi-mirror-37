from skale.contracts import BaseContract
from skale.utils.helper import format

FIELDS = ['name', 'ip', 'port', 'owner', 'start_date', 'leaving_date', 'last_reward_date', 'second_address']
#FIELDS = ['name', 'ip', 'port', 'owner', 'start_date', 'leaving_date', 'last_reward_date', 'second_address', 'status']
COMPACT_FIELDS = ['schainIndex', 'nodeID', 'ip', 'basePort']

class Nodes(BaseContract):

    def __get_raw(self, node_id):
        # return self.contract.functions.getNode(node_id).call()
        return self.contract.functions.nodes(node_id).call()

    @format(FIELDS)
    def get(self, node_id):
        return self.__get_raw(node_id)

    def get_active_node_ids(self):
        return self.contract.functions.getActiveNodeIds().call()

    def get_active_node_ips(self):
        return self.contract.functions.getActiveNodeIPs().call()

    def get_active_nodes_by_address(self, account):
        return self.contract.functions.getActiveNodesByAddress().call({'from': account})
