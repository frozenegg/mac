from info_chain import *
import uuid
from flask import Flask, request, jsonify
from flask import render_template, flash, request, redirect, url_for
import hashlib
import smtplib
import datetime

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
node_address = str(uuid.uuid4()).replace('-', '')
info_chain = InfoChain()
domain = 'localhost'

app = Flask(__name__)
email = 'infochain.yui@gmail.com'
password = ''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_mail(email, user, password, comment, transaction_id):
    message = 'You have uploaded a transaction with the comment below!\n\n' + comment + '\n\nAccess the link below to verify your transaction.\nThank you for participating in InfoChain!\n\n' + 'http://' + domain + ':5000/activation/{}'.format(transaction_id)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, user, message)
    server.quit()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/blockchain')
def blockchain():
    data = info_chain.chain
    return jsonify({
        'status':'OK',
        'data':data
    })

@app.route('/transaction', methods=["GET", "POST"])
def transaction():
    if request.method == "GET":
        return render_template('transaction_form.html')
    else:
        raw_user = request.form['user']
        user = hashlib.md5(raw_user.encode("UTF-8")).hexdigest()
        comment = request.form['comment']
        verify = False
        
        if 'file' in request.files and allowed_file(file.filename): 
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_sha256 = hashlib.sha256(file.encode("UTF-8")).hexdigest()
        else:
            file = 0
            file_sha256 = str(file)

        new_transaction = info_chain.create_new_transaction(user, comment, file_sha256, verify)
        transaction_id = new_transaction['transaction_id']
        block_index = info_chain.add_transaction_to_pending_transactions(new_transaction)

        send_mail(email, raw_user, password, comment, transaction_id)

        return render_template('to_pending.html', block_index=block_index)

@app.route('/mine')
def mine():
    last_block = info_chain.get_last_block()
    previous_block_hash = last_block['hash']
    info_chain.verify_transaction()
    current_block_data = {
        'transactions':info_chain.pending_transaction_verified,
        'index':last_block['index'] + 1
    }
    nonce = info_chain.proof_of_work(previous_block_hash, current_block_data)
    block_hash = info_chain.hash_block(previous_block_hash, current_block_data, nonce)
    new_block = info_chain.create_new_block(nonce, previous_block_hash, block_hash)

    return jsonify({
        'status':'mining complete!',
        'data':new_block
    })

@app.route('/activation/<transaction_id>')
def activation(transaction_id=None):
    activated = info_chain.activate_transaction(transaction_id)
    if activated:
        return render_template('activation.html', transaction_id=transaction_id)
    else:
        return render_template('not_activated.html', transaction_id=transaction_id)

@app.route('/get_transaction', methods=["GET", "POST"])
def get_transaction():
        if request.method == "GET":
            return render_template('get_transaction.html')
        else:
            raw_user = request.form['user']
            user = hashlib.md5(raw_user.encode("UTF-8")).hexdigest()
            user_transaction = info_chain.get_user_transaction(user)
            return jsonify({'data': user_transaction})

if __name__ == "__main__":
    app.run(debug=True, host=domain, port=5000, threaded=True)