import datetime
import uuid
import json
import hashlib

class InfoChain:
    def __init__(self):
        self.chain = []
        self.pending_transaction = []
        self.network_nodes = []
        self.pending_transaction_verified = []

        self.create_new_block(100, '0', '0')

    def create_new_block(self, nonce, previous_block_hash, hash):
        new_block = {
            'index' : len(self.chain) + 1,
            'timestamp' : datetime.datetime.now(),
            'transactions' : self.pending_transaction_verified,
            'nonce' : nonce,
            'hash' : hash,
            'previous_block_hash' : previous_block_hash
        }

        self.pending_transaction = []           # reset pending_transaction
        self.pending_transaction_verified = []
        self.chain.append(new_block)

        return new_block

    def get_last_block(self):
        return self.chain[len(self.chain) - 1]

    def create_new_transaction(self, user, comment, file_sha256, verify):
        new_transaction = {
            'user' : user,
            'comment' : comment,
            'file_sha256' : file_sha256,
            'verify' : verify,
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

    def activate_transaction(self, transaction_id):
        activated = False
        for transaction in self.pending_transaction:
            if(transaction['transaction_id'] == transaction_id):
                transaction['verify'] = True
                activated = True
        return activated

    
    def verify_transaction(self):
        for transaction in self.pending_transaction:
            if(transaction['verify'] != False):
                self.pending_transaction_verified.append(transaction)

    def get_user_transaction(self, user):
        user_transaction = []
        for block in self.chain:
            for transaction in block['transactions']:
                if(transaction['user'] == user):
                    user_transaction.append(transaction)
        return user_transaction

