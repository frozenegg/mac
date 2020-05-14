import datetime
import uuid
import json
import hashlib

class Blockchain:
    def __init__(self, current_node_url):
        self.chain = []
        self.pending_transaction = []
        self.current_node_url = current_node_url
        self.network_nodes = []

        self.create_new_block(100, '0', '0')

    def create_new_block(self, nonce, previous_block_hash, hash):
        new_block = {
            'index' : len(self.chain) + 1,
            'timestamp' : datetime.datetime.now(),
            'transactions' : self.pending_transaction,
            'nonce' : nonce,
            'hash' : hash,
            'previous_block_hash' : previous_block_hash
        }

        self.pending_transaction = [] # reset pending_transaction
        self.chain.append(new_block)

        return new_block

    def get_last_block(self):
        return self.chain[len(self.chain) - 1]

    def create_new_transaction(self, amount, sender, recipient):
        new_transaction = {
            'amount' : amount,
            'sender' : sender,
            'recipient' : recipient,
            'transaction_id' : str(uuid.uuid4()).replace('-', '')
        }

        return new_transaction

    def add_transaction_to_pending_transactions(self, transaction_obj):
        self.pending_transaction.append(transaction_obj)
        return self.get_last_block()['index'] + 1

    def hash_block(self, previous_block_hash, current_block_data, nonce):
        data_as_string = previous_block_hash + str(nonce) + json.dumps(current_block_data)
        hash = hashlib.sha256(data_as_string.encode("UTF-8")).hexdigest()
        return hash

    def proof_of_work(self, previous_block_hash, current_block_data):
        nonce = 0
        hash = self.hash_block(previous_block_hash, current_block_data, nonce)
        while(hash[0:4] != '0000'):
            nonce += 1
            hash = self.hash_block(previous_block_hash, current_block_data, nonce)

        return nonce

    def get_block(self, block_hash):
        correct_block = None
        for block in self.chain:
            if(block['hash'] == block_hash):
                correct_block = block

        return correct_block

    def get_transaction(self, transaction_id):
        correct_transaction = None
        correct_block = None

        # for block in self.chain:

    def get_address_data (self, address):
        address_transaction = []

        # for block in self.chain:



blockchain = Blockchain('1')
print(blockchain.chain)
