from flask import Flask, request, redirect, jsonify
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
from json import loads, dumps
from os import urandom
from datetime import datetime
from yaml import load, FullLoader

app = Flask(__name__)
mysql = MySQL(app)

# MySQL Configuration
db = load(open('db.yaml'), Loader=FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['CURSOR_CLASS'] = DictCursor
app.config['SECRET_KEY'] = urandom(24)

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, data')
    return response

@app.route('/', methods=['GET'])
def index():
    return "Google Keep Backend"

@app.route('/get')
def get():
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT * FROM keeps;")
    if q > 0:
        keeps = cur.fetchall()
        result = []
        for keep in keeps:
            result.append({
                'id'        : keep[0],
                'title'     : keep[1],
                'body'      : keep[2],
                'important' : keep[3]
            })
            print(keep)
            print('--------------------')
        return jsonify({'response': 'success', 'message': 'Keeps Loaded Successfully', 'keeps': result})
    else:
        return jsonify({'response' : 'error', 'message': "No Database Entries Found", 'keeps': int(q)})

@app.route('/new', methods=['POST'])
def post():
    if request.method == 'POST':
        result = request.json
        title = str(result['title'])
        body = str(result['body'])
        important = bool(result['important'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO keeps(title, body, important) VALUES(%s, %s, %b);", (title, body, important))
        mysql.connection.commit()
        cur.close()
    return jsonify({'status': 'OK', 'message': 'Posted Successfully'})

@app.route('/delete', methods=['POST'])
def delete():
    result = request.json
    id = result['id']
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM keeps WHERE id={};'.format(int(id)))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)