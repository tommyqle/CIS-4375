# Before first run do:
# pip install mysql.connector
# pip install npm
# npm install flask
# Run by:
# python start.py

import flask
import json
from flask import request, make_response, jsonify
from sql import create_connection, execute_query, execute_read_query
import creds

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create connection to MySQL database
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

# View table in database
@app.route('/overview', methods=['GET'])
def test_view():
    tableSelect = "inventory"
    sqlSelect = "SELECT * FROM %s" % (tableSelect)
    viewTable = execute_read_query(conn, sqlSelect)
    return jsonify(viewTable)

# Test input data to database
@app.route('/api/testadd', methods=['POST'])
def testAdd():
    testData = request.json.get("name")

    post_statement = "INSERT INTO test (name) VALUES ('%s')" % (testData)
    execute_query(conn, post_statement)
    return "Successfully added!"


app.run()