#!/usr/bin/python3.6

from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from os import urandom
from yaml import load, FullLoader

app = Flask(__name__)
mysql = MySQL(app)

# MySQL Configuration
db_keeps = load(open('keeps_db.yaml'), Loader=FullLoader)
app.config['MYSQL_HOST'] = db_keeps['mysql_host']
app.config['MYSQL_USER'] = db_keeps['mysql_user']
app.config['MYSQL_PASSWORD'] = db_keeps['mysql_password']
app.config['MYSQL_DB'] = db_keeps['mysql_db']
app.config['SECRET_KEY'] = urandom(24)

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, data')
    return response

@app.route('/')
def index():
    return jsonify({
        'response': 'success',
        'message': 'This is the home route for All the Apps made by Yuvraj Dagur',
        'apps': [
            {"Google Keep": "/keeps"}
        ]
    })

@app.route('/keeps', methods=['GET'])
def keeps():
    return jsonify({
        'response'  : 'success',
        'message'   : 'Google Keep Clone Backend by Yuvraj Dagur',
        'routes'    : ['/get', '/new', '/delete', '/edit']
        })

@app.route('/keeps/get')
def get():
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT * FROM keeps ORDER BY keep_id DESC;")
    if q > 0:
        keeps = cur.fetchall()
        result = []
        for keep in keeps:
            result.append({
                'id'        : keep[0],
                'title'     : keep[1],
                'body'      : keep[2],
                'date_time' : keep[3],
                'color'     : keep[4],
                'important' : keep[5],
                'edited'    : keep[6]
            })
        return jsonify({
            'response'  : 'success',
            'message'   : 'Keeps Loaded Successfully',
            'keeps'     : result
            })
    else:
        return jsonify({'response' : 'error', 'message': "No Database Entries Found", 'keeps': int(q)})

@app.route('/keeps/new', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        result = request.json
        title = str(result['title'])
        body = str(result['body'])
        important = bool(result['important'])
        color = str(result['color'])
        date_time = str(result["date_time"])
        edited = 0
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO keeps(title, body, date_time, color, important, edited) VALUES(%s, %s, %s, %s, %b, %b);", (title, body, date_time, color, important, edited))
        mysql.connection.commit()
        cur.close()
        return jsonify({
            'response'  : 'success',
            'message'   : 'Posted Successfully',
            'content'   : {
                'title'     : title,
                'important' : important,
                'body'      : body,
                'color'     : color,
                'important' : important,
                'edited'    : bool(edited)
                }
        })
    else:
        return jsonify({
            'response'  : 'success',
            'message'   : "This route will be used to create a new Note. Make a POST Request to this route using parameters {'id', 'title', 'body', 'date_time', 'color', 'important', 'edited'}"
        })

@app.route('/keeps/delete', methods=['POST'])
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

@app.route('/keeps/edit', methods=['POST'])
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