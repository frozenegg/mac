from chain import *
import uuid
from flask import Flask, request, jsonify
from flask import render_template, flash, request, redirect, url_for
import hashlib
import smtplib
import datetime
from werkzeug.utils import secure_filename
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import requests
import json
import os
import yaml

domain = 'localhost'
# proper_domain = 'http://localhost:5000'
proper_domain = 'https://46ad2cb74261.ngrok.io'

access_token = ''
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler('')

email = 'infochain.yui@gmail.com'
password = ''

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
API_URL = 'https://notify-api.line.me/api/notify'
info_chain = InfoChain()

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_mail(user, message):
    message = message
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, user, message)
    server.quit()

def send_mail_for_bookdata(user, book_id, add_book_id):
    message = 'You have uploaded a transaction with the book below!\n\n' + book_id + '\n\nAccess the link below to verify your transaction.\nThank you for participating in InfoChain!\n\n' + proper_domain + '/activation/{}'.format(add_book_id)
    send_mail(user, message)

def send_mail_transaction(user, book_id, transaction_id, person):
    message = 'You have uploaded a transaction with the book below!\n\n' + book_id + '\n\nAccess the link below to verify your transaction.\nThank you for participating in InfoChain!\n\n' + proper_domain + '/activation{}/{}'.format(person, transaction_id)
    send_mail(user, message)

def send_mail_request_activation(user1, user2_md5, book_id):
    user1_md5 = hashlib.md5(user1.encode("UTF-8")).hexdigest()
    message = 'Click the link below to send offer to the seller\n' + 'book id: ' + book_id + '\n' + proper_domain + '/activation3/{}-{}-{}'.format(user1_md5, user2_md5, book_id)
    send_mail(user1, message)

def send_mail_add_user(email, line_id_md5):
    message = 'Click the link below to activate user!\n\n' + proper_domain + '/activation4/{}'.format(line_id_md5)
    send_mail(email, message)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

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
        raw_user1 = request.form['user1']
        raw_user2 = request.form['user2']
        user1 = hashlib.md5(raw_user1.encode("UTF-8")).hexdigest()
        user2 = hashlib.md5(raw_user2.encode("UTF-8")).hexdigest()
        assessment = request.form['assessment']
        verification1 = False
        verification2 = False
        book_id = request.form['book_id']

        if request.form['comment']:
            comment = request.form['comment']
        else:
            comment = 'No comment'

        new_transaction = info_chain.create_new_transaction(user1, user2, assessment, book_id, verification1, verification2, comment)
        transaction_id = new_transaction['transaction_id']
        modified_bookdata = info_chain.create_new_bookdata(user1, book_id, '', False, True, 'sold')
        block_index = info_chain.add_transaction_to_pending_transactions(new_transaction)
        block_index_duplicate = info_chain.add_transaction_to_pending_transactions(modified_bookdata)

        send_mail_transaction(raw_user1, book_id, transaction_id, 1)
        send_mail_transaction(raw_user2, book_id, transaction_id, 2)

        return render_template('to_pending.html', block_index=block_index)

@app.route('/mine')
def mine():
    last_block = info_chain.get_last_block()
    previous_block_hash = last_block['hash']
    info_chain.verification()
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

@app.route('/activation/<add_book_id>')
def activation(add_book_id=None):
    user_md5 = add_book_id.split('-')[0]
    book_id = add_book_id.split('-')[1]
    activated = info_chain.activate_bookdata(user_md5, book_id)
    if activated:
        return render_template('activation.html', transaction_id=book_id)
    else:
        return render_template('not_activated.html', transaction_id=book_id)

@app.route('/activation1/<transaction_id>')
def activation1(transaction_id=None):
    activated = info_chain.activate_transaction1(transaction_id)
    if activated:
        return render_template('activation.html', transaction_id=transaction_id)
    else:
        return render_template('not_activated.html', transaction_id=transaction_id)

@app.route('/activation2/<transaction_id>')
def activation2(transaction_id=None):
    activated = info_chain.activate_transaction2(transaction_id)
    if activated:
        return render_template('activation.html', transaction_id=transaction_id)
    else:
        return render_template('not_activated.html', transaction_id=transaction_id)

@app.route('/activation3/<user_book_id>')
def actication3(user_book_id=None):
    user1_md5, user2_md5, book_id = user_book_id.split('-')



    return user1_md5

@app.route('/activation4/<line_id_md5>')
def add_user(line_id_md5=None):
    with open('data/' + line_id_md5 + '.json', 'r') as f:
        data = json.load(f)
        data_jsonified = yaml.load(data)
        data_jsonified['verification'] = True

    line_bot_api.push_message(data_jsonified['line_id'], TextSendMessage(text='認証が完了しました。'))

    with open('data/' + line_id_md5 + '.json', 'w') as f:
        json.dump(data_jsonified, f)

    return 'User activated successfully.'

@app.route('/get_user_transaction', methods=["GET", "POST"])
def get_user_transaction():
    if request.method == "GET":
        return render_template('get_user_transaction.html')
    else:
        raw_user = request.form['user']
        user = hashlib.md5(raw_user.encode("UTF-8")).hexdigest()
        user_transaction = info_chain.get_user_transaction(user)
        return jsonify({'data': user_transaction})

@app.route('/get_user_bookdata', methods=["GET", "POST"])
def get_user_bookdata():
    if request.method == "GET":
        return render_template('get_user_bookdata.html')
    else:
        raw_user = request.form['user']
        user = hashlib.md5(raw_user.encode("UTF-8")).hexdigest()
        user_bookdata = info_chain.get_user_bookdata(user)
        return jsonify({'bookdata': user_bookdata})

@app.route('/get_bookdata', methods=["GET", "POST"])
def get_bookdata():
    if request.method == "GET":
        return render_template('get_bookdata.html')
    else:
        book_id = request.form['book_id']
        bookdata = info_chain.get_bookdata(book_id)
        return jsonify({'data':bookdata})

@app.route('/add_book', methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        return render_template('add_book.html')
    else:
        raw_user = request.form['user']
        user = hashlib.md5(raw_user.encode("UTF-8")).hexdigest()
        book_id = request.form['book_id']

        user_bookdata = info_chain.get_user_bookdata(user)
        user_books = []
        for book in user_bookdata:
        	user_books.append(book['book_id'])
        if(book_id not in user_books):
	        file = request.files['file']
	        
	        if 'file' in request.files and allowed_file(file.filename): 
	            filename = secure_filename(file.filename)
	            quality = hashlib.sha256(filename.encode("UTF-8")).hexdigest()
	        else:
	            quality = None

	        on_sale = True
	        verification = False
	        price = request.form['price']

	        new_book = info_chain.create_new_bookdata(user, book_id, quality, on_sale, verification, price)

	        block_index = info_chain.add_transaction_to_pending_transactions(new_book)

	        add_book_id = str(user) + '-' + str(book_id)

	        send_mail_for_bookdata(raw_user, book_id, add_book_id)
	        return render_template('added_bookdata.html', book_id=book_id)    
        else:
        	return render_template('same_book.html', book_id=book_id)

@app.route('/cancel_upload', methods=["GET", "POST"])
def cancel_upload():
	if request.method == "GET":
		return render_template('cancel_upload.html')
	else:
		raw_user = request.form['user']
		user = hashlib.md5(raw_user.encode("UTF-8")).hexdigest()
		book_id = request.form['book_id']

		quality = None
		on_sale = False
		verification = False
		price = 'withdrawn'
		new_book = info_chain.create_new_bookdata(user, book_id, quality, on_sale, verification, price)

		block_index = info_chain.add_transaction_to_pending_transactions(new_book)
		add_book_id = str(user) + '-' + str(book_id)

		send_mail_for_bookdata(raw_user, book_id, add_book_id)
		return render_template('added_bookdata.html', book_id=book_id)

@app.route('/send_request', methods=["GET", "POST"])
def send_request():
    if request.method == "GET":
        return render_template('send_request.html')
    else:
        user1 = request.form['user1']
        user2_md5 = request.form['user2_md5']
        book_id = request.form['book_id']
        price_offer = request.form['price_offer']
        place = request.form['place']

        send_mail_request_activation(user1, user2_md5, book_id)

        return render_template('request_activation_sent.html')

@app.route('/callback', methods=['POST'])
def callback():
    if request.method == 'POST':
        events = request.json['events']
        line_user_id = events[0]['source']['userId']
        message = events[0]['message']['text']

        line_id_md5 = hashlib.md5(line_user_id.encode("UTF-8")).hexdigest()

        if('@st.kyoto-u.ac.jp' in message):
            info_chain.add_user(message, line_user_id)
            send_mail_add_user(message, line_id_md5)
            line_bot_api.push_message(line_user_id, TextSendMessage(text='学内メール宛に確認メールを送信しました。\nリンクを開いてユーザーを有効化してください。\n\n間違えた場合は正しいアドレスをもう一度送信してください。'))

    return 'OK' 

@app.route('/kill_process/<passwd>')
def kill_process(passwd=None):
    password1 = hashlib.sha256(password.encode("UTF-8")).hexdigest()
    if(passwd == password1):
        info_chain.save_chain()
        shutdown_server()
        return 'Chain dumped.Server shutting down...'
    else:
        return 'No permission'

if __name__ == "__main__":
    app.run(debug=True, host=domain, port=5000, threaded=True)

