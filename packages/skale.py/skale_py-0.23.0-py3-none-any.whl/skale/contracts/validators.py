from skale.contracts import BaseContract


class Validators(BaseContract):

    def get_periods(self, account):
        return self.contract.functions.getPeriods().call({'from': account})

    def get_validated_array(self, node_id, account):
        return self.contract.functions.getValidatedArray(node_id).call({'from': account})