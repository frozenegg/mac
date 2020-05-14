from blockchain import *
import uuid
import http.server
from flask import Flask, request, jsonify
from flask import render_template
import hashlib

node_address = str(uuid.uuid4()).replace('-', '')
blockchain = Blockchain("1")

app = Flask(__name__)

@app.route('/blockchain')
def asdf():
    data = blockchain.chain
    return jsonify({
        'status':'OK',
        'data':data
    })

@app.route('/transaction', methods=["GET", "POST"])
def transaction():
    if request.method == "GET":
        return render_template('transaction_form.html')
    else:
        amount = request.form['amount']
        sender = request.form['sender']
        recipient = request.form['recipient']
        new_transaction = blockchain.create_new_transaction(amount, sender, recipient)
        block_index = blockchain.add_transaction_to_pending_transactions(new_transaction)
        return render_template('to_pending.html', block_index=block_index)

@app.route('/mine')
def mine():
    last_block = blockchain.get_last_block()
    previous_block_hash = last_block['hash']
    current_block_data = {
        'transactions':blockchain.pending_transaction,
        'index':last_block['index'] + 1
    }
    nonce = blockchain.proof_of_work(previous_block_hash, current_block_data)
    block_hash = blockchain.hash_block(previous_block_hash, current_block_data, nonce)
    new_block = blockchain.create_new_block(nonce, previous_block_hash, block_hash)

    return jsonify({
        'status':'mining complete!',
        'data':new_block
    })

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000, threaded=True)
