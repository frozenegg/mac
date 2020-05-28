import datetime
import uuid
import json
import hashlib
import collections
import yaml

class InfoChain:
    def __init__(self):
        self.chain = []
        self.pending_transaction = []
        self.network_nodes = []
        self.pending_transaction_verified = []

        if(len(self.chain) == 0):
            self.create_new_block(100, '0', '0')
        else:
            with open('blockchain.json', 'r') as f:
                saved_json_string = json.load(f, object_pairs_hook=collections.OrderedDict)
                saved_json = yaml.load(saved_json_string)

            for block in saved_json['chain']:
                self.chain.append(block)      

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
        self.save_chain()

        return new_block

    def get_last_block(self):
        return self.chain[len(self.chain) - 1]

    def create_new_transaction(self, user1_md5, user2_md5, assessment, book_id, verification1, verification2, comment):
        new_transaction = {
            'seller' : user1_md5,
            'buyer' : user2_md5,
            'assessment' : assessment,
            'book_id' : book_id,
            'verification1' : verification1,
            'verification2' : verification2,
            'comment_from_buyer' : comment,
            'transaction_id' : str(uuid.uuid4()).replace('-', '')
        }

        return new_transaction

    def create_new_bookdata(self, user_md5, book_id, quality, on_sale, verification, price):
        new_book = {
            'user' : user_md5,
            'book_id' : book_id,
            'quality' : quality,
            'on_sale' : on_sale,
            'verification' : verification,
            'price' : price
        }

        return new_book

    def add_transaction_to_pending_transactions(self, transaction_obj):
        self.pending_transaction.append(transaction_obj)
        return self.get_last_block()['index'] + 1

    def hash_block(self, previous_block_hash, current_block_data, nonce):
        data_as_string = previous_block_hash + str(nonce) + json.dumps(current_block_data)
        hash = hashlib.md5(data_as_string.encode("UTF-8")).hexdigest()
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

    def activate_bookdata(self, user_md5, book_id):
        activated = False
        for book in self.pending_transaction:
            if('user' in book.keys() and book['book_id'] == book_id and book['user'] == user_md5):
                book['verification'] = True
                activated = True
        return activated

    def activate_transaction1(self, transaction_id):
        activated = False
        for transaction in self.pending_transaction:
            if('transaction_id' in transaction.keys() and transaction['transaction_id'] == transaction_id):
                transaction['verification1'] = True
                activated = True
        return activated

    def activate_transaction2(self, transaction_id):
        activated = False
        for transaction in self.pending_transaction:
            if('transaction_id' in transaction.keys() and transaction['transaction_id'] == transaction_id):
                transaction['verification2'] = True
                activated = True
        return activated

    def verification(self):
        for transaction in self.pending_transaction:
            if('verification' in transaction.keys() and transaction['verification'] == True):
                self.pending_transaction_verified.append(transaction)
            elif(('verification1' in transaction.keys()) and ('verification2' in transaction.keys()) and (transaction['verification1'] == True) and (transaction['verification2'] == True)):
                self.pending_transaction_verified.append(transaction)

    def get_user_transaction(self, user_md5):
        user_transaction = []
        for block in reversed(self.chain):
            for transaction in reversed(block['transactions']):
                if(('user1' in transaction.keys() and transaction['user1'] == user_md5 or transaction['user2']) or 'user' in transaction.keys() and transaction['user'] == user_md5) :
                    user_transaction.append(transaction)
        return user_transaction

    def get_user_bookdata(self, user_md5):
        user_bookdata = []
        for block in reversed(self.chain):
            for bookdata in reversed(block['transactions']):
                if('user' in bookdata.keys() and bookdata['user'] == user_md5):
                    user_bookdata.append(bookdata)
        return self.delete_same_book(user_bookdata)

    def get_bookdata(self, book_id):
        bookdatas = []
        for block in reversed(self.chain):
            for bookdata in reversed(block['transactions']):
                if('on_sale' in bookdata.keys() and bookdata['book_id'] == book_id):
                    bookdatas.append(bookdata)
        return self.delete_same_book(bookdatas)

    def delete_same_book(self, bookdata):
    	user_plus_bookids_dict = {}
    	modified_bookdata = []
    	for book in reversed(bookdata):
    		user_plus_bookid = str(book['user']) + '-' + str(book['book_id'])
    		user_plus_bookids_dict[user_plus_bookid] = book
    	for book_dict in user_plus_bookids_dict:
    		modified_bookdata.append(user_plus_bookids_dict[book_dict])

    	return modified_bookdata

    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def save_chain(self):
        saved_chain ={
            'timestamp' : datetime.datetime.now(),
            'chain': self.chain
        }
        json_chain = json.dumps(saved_chain, default=self.myconverter)
        with open('blockchain.json', 'w') as f:
            json.dump(json_chain, f)




