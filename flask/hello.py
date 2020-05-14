from flask import Flask, request, jsonify
from flask import render_template
import pymysql

app = Flask(__name__)

@app.route('/')
def hello():
    name = "hoge"
    # return name
    return render_template('hello.html', title='flask test', name=name)

    # db = pymysql.connect(
    #     host='localhost',
    #     user='root',
    #     password='root',
    #     db='testdb',
    #     charset='utf8',
    #     cursorclass=pymysql.cursors.DictCursor
    # )
    #
    # cur = db.cursor()
    # sql = "select * from members"
    # cur.execute(sql)
    # members = cur.fetchall()
    #
    # cur.close()
    # db.close()
    #
    # return render_template('hello2.html', title='flask test', members=members)

@app.route('/hello/<name>')
def hello3(name=None):
    return render_template('hello.html', title='flask test', name=name)

@app.route('/hello4', methods=['GET', 'POST'])
def hello4():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = "no name."
    return render_template('hello4.html', title='flask test', name=name)

@app.route("/odd_even", methods=["GET", "POST"])
def odd_even():
    if request.method == "GET":
        return """
        下に整数を入力してください。奇数か偶数か判定します
        <form action="/odd_even" method="POST">
        <input name="num"></input>
        </form>"""
    else:
        try:
            return """
            {}は{}です！
            <form action="/odd_even" method="POST">
            <input name="num"></input>
            </form>""".format(str(request.form["num"]), ["偶数", "奇数"][int(request.form["num"]) % 2])
        except:
            return """
                    有効な数字ではありません！入力しなおしてください。
                    <form action="/" method="POST">
                    <input name="num"></input>
                    </form>"""

@app.route('/hello5')
def hello5():
    name = request.args.get('name')
    return render_template('hello.html', title='flask test', name=name)
    # http://localhost:5000hello?name=hoge

# Return JSON
app.config['JSON_AS_ASCII'] = False # For Japanese character
app.config['JSON_SORT_KEYS'] = False # Keep sorted

@app.route('/json')
def json():
    data = [
        {"name":"齊藤"},
        {"age":21}
    ]
    return jsonify({
        'status':'OK',
        'data':data
    })

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='testdb',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor,
    )

# @app.route('/pymysql')
# def sql():
#     db = get_connection()
#     cur = db.cursor()
#     sql = "select * from members"
#     cur.execute(sql)
#     members = cur.fetchall()
#     cur.close()
#     db.close()
#
#     return jsonify({
#         'status':'OK',
#         'members':members
#     })


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000, threaded=True)
