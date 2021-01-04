from flask import Flask, request, redirect, jsonify
from flask_mysqldb import MySQL
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

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, data')
    return response

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'response'  : 'success', 
        'message'   : 'Google Keep Clone Backend by Yuvraj Dagur', 
        'routes'    : ['/get', '/new', '/delete', '/edit']
        })

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
                'important' : keep[3],
                'color'     : keep[4]
            })
        return jsonify({
            'response'  : 'success', 
            'message'   : 'Keeps Loaded Successfully', 
            'keeps'     : result
            })
    else:
        return jsonify({'response' : 'error', 'message': "No Database Entries Found", 'keeps': int(q)})

@app.route('/new', methods=['POST'])
def post():
    if request.method == 'POST':
        result = request.json
        title = str(result['title'])
        body = str(result['body'])
        important = bool(result['important'])
        color = str(result['color'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO keeps(title, body, important, color) VALUES(%s, %s, %b, %s);", (title, body, important, color))
        mysql.connection.commit()
        cur.close()
    return jsonify({
        'response'  : 'success', 
        'message'   : 'Posted Successfully', 
        'content'   : {
            'title'     : title,
            'important' : important,
            'body'      : body,
            'color'     : color
            }
        })

@app.route('/delete', methods=['POST'])
def delete():
    result = request.json
    id = result['id']
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM keeps WHERE keep_id={};'.format(int(id)))
    mysql.connection.commit()
    cur.close()
    return jsonify({
        'response'  : 'success', 
        'message'   : 'Deleted Successfully',
        'content'   : 'Deleted Note ID' + str(id)
        })

@app.route('/edit', methods=['POST'])
def edit():
    result = request.json
    id = int(result['id'])
    title = str(result['title'])
    body = str(result['body'])
    important = bool(result['important'])
    color = str(result['color'])
    cur = mysql.connection.cursor()
    cur.execute("UPDATE keeps SET title={}, body={}, important={}, color={} WHERE keep_id={};".format(title, body, important, color, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({
        'response': 'success', 
        'message': 'Entries Updated',
        'content'   : {
            'title'     : title,
            'body'      : body,
            'important' : important,
            'color'     : color
            }
        })

@app.errorhandler(404)
def error(e):
    return jsonify({
        'response'  : 'failure', 
        'error'     : '404', 
        'message'   : str(e)
        })


if __name__ == '__main__':
    app.run(debug=True)