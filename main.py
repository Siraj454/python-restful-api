import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>British Trafic Police Data</h1>
<p>An API for British Trafic Police Crime Data.</p>
<p>Api to fetch whole data: http://127.0.0.1:5000/api/v1/resources/btp_data_base/all.</p>
<h2> Filter by Month<h2>
<p>http://127.0.0.1:5000/api/v1/resources/btp_data_base?Month=2020-08<p>
'''


@app.route('/api/v1/resources/btp_data_base/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('output2.sqlite')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_data = cur.execute('SELECT * FROM btp_data_base;').fetchall()

    return jsonify(all_data)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/btp_data_base', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('index')
    location = query_parameters.get('Location')
    month = query_parameters.get('Month')


    query = "SELECT * FROM btp_data_base WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if location:
        query += ' location=? AND'
        to_filter.append (location)
    if month:
        query += ' month=? AND'
        to_filter.append(month)
    if not (id or location or month):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('output2.sqlite')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()