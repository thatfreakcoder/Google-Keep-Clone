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
app.config['SECRET_KEY'] = urandom(24)
app.config['CURSORCLASS'] = DictCursor

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
    query_res = cur.execute("SELECT * FROM keeps;")
    if query_res > 0:
        query_num = cur.fetchall()
        return str(query_num)
    else:
        return "None"

@app.route('/new', methods=['POST'])
def post():
    if request.method == 'POST':
        result = request.json
        title = result['title']
        body = result['body']
        date_time = result['date_time']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO keeps(heading, body, date_time) VALUES(%s, %s, %s);", (title, body, date_time))
        mysql.connection.commit()
        cur.close()
    return redirect('/')

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