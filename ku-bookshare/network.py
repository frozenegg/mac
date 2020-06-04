from chain import *
import uuid
from flask import Flask, request, jsonify, render_template, flash, request, redirect, url_for, send_from_directory
import hashlib
import smtplib
from datetime import datetime
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
from glob import glob
import yaml
import os
import uuid as myuuid
from email.mime.text import MIMEText

domain = 'localhost'
# proper_domain = 'http://localhost:5000'
proper_domain = 'https://a4971417a44e.ngrok.io'

access_token = ''
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler('')

email = 'infochain.yui@gmail.com'
password = ''

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
API_URL = 'https://notify-api.line.me/api/notify'

app = Flask(__name__)

info_chain = InfoChain()

def send_mail(user, message):
    jp='iso-2022-jp'
    msg = MIMEText(message.encode(jp), 'plain', jp,)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, user, str(msg))
    server.quit()

def send_mail_for_bookdata(user, book_id, add_book_id):
    message = 'You have uploaded a transaction with the book below!\n\n' + book_id + '\n\nAccess the link below to verify your transaction.\nThank you for participating in InfoChain!\n\n' + proper_domain + '/activation/{}'.format(add_book_id)
    send_mail(user, message)

def send_mail_transaction(user, book_id, transaction_id, person):
    message = 'You have uploaded a transaction with the book below!\n\n' + book_id + '\n\nAccess the link below to verify your transaction.\nThank you for participating in InfoChain!\n\n' + proper_domain + '/activation{}/{}'.format(person, transaction_id)
    send_mail(user, message)

def send_mail_request_activation(user1, user2_md5, book_id, price):
    user1_md5 = hashlib.md5(user1.encode("UTF-8")).hexdigest()
    message = 'Click the link below to send offer to the seller\n' + 'book id: ' + book_id + '\n' 'price: ' + price + '\n' + proper_domain + '/activation3/{}-{}-{}'.format(user1_md5, user2_md5, book_id)
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
    return render_template('index.html')

@app.route('/blockchain')
def blockchain():
    data = info_chain.chain
    return jsonify({
        'status':'OK',
        'data':data
    })

@app.route('/transaction/<chatid>', methods=["GET", "POST"])
def transaction(chatid=None):
    uuid, book_id = chatid.split('-')

    with open('chat/' + chatid + '.json', 'r') as f:
        message_json = json.load(f)
        message = []
        for message_json in message_json:
            message.append(message_json)
    user1_line_id = message[0]
    user2_line_id = message[1]
    user1_line_md5 = hashlib.md5(user1_line_id.encode("UTF-8")).hexdigest()
    user2_line_md5 = hashlib.md5(user2_line_id.encode("UTF-8")).hexdigest()

    try:
        with open('data/' + user1_line_md5 + '.json', 'r') as f:
            data = json.load(f)
            email1 = data['email']
    except:
        with open('data/' + user1_line_md5 + '.json', 'r') as f:
            data =json.load(f)
            email1 = data['email']

    try:
        with open('data/' + user2_line_md5 + '.json', 'r') as f:
            data = json.load(f)
            email2 = data['email']
    except:
        with open('data/' + user2_line_md5 + '.json', 'r') as f:
            data =json.load(f)
            email2 = data['email']

    user1_email_md5 = hashlib.md5(email1.encode("UTF-8")).hexdigest()
    user2_email_md5 = hashlib.md5(email2.encode("UTF-8")).hexdigest()

    if request.method == "GET":
        return render_template('transaction_form.html')
    else:
        raw_user2 = request.form['user2']
        if request.form['comment']:
            comment = request.form['comment']
        else:
            comment = 'No comment'

        assessment = request.form['assessment']

        if(raw_user2 == email2):
            user1 = hashlib.md5(email1.encode("UTF-8")).hexdigest()
            user2 = hashlib.md5(raw_user2.encode("UTF-8")).hexdigest()

            verification1 = False
            verification2 = False

            new_transaction = info_chain.create_new_transaction(user1, user2, assessment, book_id, verification1, verification2, comment)
            transaction_id = new_transaction['transaction_id']
            modified_bookdata = info_chain.create_new_bookdata(user1, book_id, '', False, True, 'sold', '')
            block_index = info_chain.add_transaction_to_pending_transactions(new_transaction)
            block_index_duplicate = info_chain.add_transaction_to_pending_transactions(modified_bookdata)

            send_mail_transaction(email1, book_id, transaction_id, 1)
            send_mail_transaction(raw_user2, book_id, transaction_id, 2)

            line_bot_api.push_message(user1_line_id, TextSendMessage(text='下のリンクをタップして\n\n　' + book_id + '\n\nの取引を確認してください。\n' + proper_domain + '/activation1/{}'.format(transaction_id)))
            line_bot_api.push_message(user2_line_id, TextSendMessage(text='下のリンクをタップして\n\n　' + book_id + '\n\nの取引を確認してください。\n' + proper_domain + '/activation2/{}'.format(transaction_id)))

            transaction_url = '/transaction/' + chatid
            return render_template('to_pending.html', transaction_url=transaction_url)
        else:
            return render_template('not_valid_email.html')

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
    chat_uuid = str(myuuid.uuid4()).replace('-', '')

    for file in glob('data' + '/*.json'):
        with open(file, 'r') as f:
            user_file = json.load(f)
            email = user_file['email']
            email_md5 = hashlib.md5(email.encode("UTF-8")).hexdigest()

        if(email_md5 == user2_md5):
            user2_email = email
            user2_file = user_file
        if(email_md5 == user1_md5):
            user1_email = email
            user1_file = user_file

    message = 'Received request for ' + book_id + ' !\nHit the link below to start your deal!\n' + proper_domain + '/chat/{}-{}'.format(chat_uuid, book_id)
    send_mail(user2_email, message)

    chatid = '{}-{}'.format(chat_uuid, book_id)
    user1_line_id = user1_file['line_id']
    user2_line_id = user2_file['line_id']
    message = []
    message.append(user2_line_id)
    message.append(user1_line_id)
    with open('chat/' + chatid + '.json', 'w') as f:
        json.dump(message, f)

    if(user2_file['verification'] == True):
        line_bot_api.push_message(user2_line_id, TextSendMessage(text='{}　の取引リクエストが届きました！\n取引する場合は下のリンクから始められます！\n'.format(book_id) + proper_domain + '/chat/{}-{}'.format(chat_uuid, book_id)))
    if(user1_file['verification'] == True):
        line_bot_api.push_message(user1_line_id, TextSendMessage(text='{}　の取引リクエストを送信しました！\n下のリンクから取引チャットを開けます！\n'.format(book_id) + proper_domain + '/chat/{}-{}'.format(chat_uuid, book_id)))
    return redirect(proper_domain + '/chat/{}-{}'.format(chat_uuid, book_id))


@app.route('/activation4/<line_id_md5>')
def add_user(line_id_md5=None):
    try:
        with open('data/' + line_id_md5 + '.json', 'r') as f:
            data = json.load(f)
            data_jsonified = yaml.load(data)
            data_jsonified['verification'] = True
    except:
        with open('data/' + line_id_md5 + '.json', 'r') as f:
            data =json.load(f)
            data['verification'] = True

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
        subject = request.form['subject']
        bookdata = info_chain.get_bookdata(subject)
        return jsonify({'data':bookdata})

@app.route('/add_book', methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        return render_template('add_book.html')
    else:
        raw_user = request.form['user']
        user = hashlib.md5(raw_user.encode("UTF-8")).hexdigest()
        book_id = request.form['book_id']
        subject = request.form['subject']

        user_bookdata = info_chain.get_user_bookdata(user)
        user_books = []
        for book in user_bookdata:
        	user_books.append(book['book_id'])
        if(book_id not in user_books):
	        quality = request.form['quality']
	        on_sale = True
	        verification = False
	        price = request.form['price']

	        new_book = info_chain.create_new_bookdata(user, book_id, quality, on_sale, verification, price, subject)

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
        price = request.form['price']
        place = request.form['place']

        domain = user1.split('@')[1]

        if(domain == 'st.kyoto-u.ac.jp'):
            send_mail_request_activation(user1, user2_md5, book_id, price)

            return render_template('request_activation_sent.html')
        else:
            return render_template('use_gakunai.html')

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
        return 'Chain dumped. Server shutting down...'
    else:
        return 'No permission'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico', )

@app.route('/team.html')
def team():
	return render_template('team.html')

@app.route("/chat/<chatid>", methods=["GET", "POST"])
def chat(chatid=None):
    uuid, book_id = chatid.split('-')

    with open('chat/' + chatid + '.json', 'r') as f:
        message_json = json.load(f)
        message = []
        for message_json in message_json:
            message.append(message_json)
    message_modified = message[2:]

    if request.method == 'GET':
        msg = book_id + "の取引チャット"
        transaction_url = '../transaction/' + chatid
        return render_template("chat.html",
                               title="掲示板アプリ",
                               message=msg,
                               transaction_url=transaction_url,
                               post_message=message_modified,
                               )
    else:
        pm = request.form["post_message"]
        message.append(pm)
        with open('chat/' + chatid + '.json', 'w') as f:
            json.dump(message, f)
        line_bot_api.push_message(message[0], TextSendMessage(text=book_id + 'の取引メッセージ\n\n' + pm + '\n\n' + proper_domain + '/chat/' + chatid))
        line_bot_api.push_message(message[1], TextSendMessage(text=book_id + 'の取引メッセージ\n\n' + pm + '\n\n' + proper_domain + '/chat/' + chatid))
        return redirect("/chat/" + chatid)

if __name__ == "__main__":
    app.run(debug=True, host=domain, port=5000, threaded=True)
