# Before first run do:
# pip install mysql.connector
# pip install npm
# npm install flask
# Run by:
# python start.py

import hashlib
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

# Login with Password
@app.route('/api/login', methods=['GET'])
def usernamepw():
    # SQL query to put all users in a list
    sqlSelect = "SELECT * FROM users"
    authorizedusers = execute_read_query(conn, sqlSelect)

    # Get username/password from frontend
    authentication = request.get_json()

    # Set variables from frontend json
    username = authentication['username']
    password = authentication['password']
    # SHA256 Hash password
    hashedPassword = hashlib.sha256(password.encode())

    # Check against all users for match on both username/password
    for auth in authorizedusers:
        # If username matches and decrypted password matches
        if auth['username'] == username and auth['password'] == hashedPassword.hexdigest():
            return 'SUCCESS!'
        return 'INVALID LOGIN'

# View table in database
@app.route('/api/testview', methods=['GET'])
def test_view():
    tableSelect = "test"
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