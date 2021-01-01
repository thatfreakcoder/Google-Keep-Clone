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

@app.route('/')
def get():
    cur = mysql.connection.cursor()
    query = cur.execute("SELECT * FROM keeps")
    if query > 0:
        u_query = cur.fetchall()
        print(type(u_query))
    #     new = {'status' : 'OK'}
    #     for index, que in enumerate(u_query):
    #         res = {}
    #         res['id'] = que[0]
    #         res['title'] = que[1]
    #         res['body'] = que[2]
    #         res['date_time'] = que[3]
    #         new[] = res
    #     cur.close()
    cur.close()
    return str(u_query)

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