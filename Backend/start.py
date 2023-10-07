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

# View inventory table in database
@app.route('/api/inventory', methods=['GET'])
def viewInven():
    sqlSelect = "SELECT * FROM inventory"
# View table in database
@app.route('/overview', methods=['GET'])
def test_view():
    tableSelect = "inventory"
    sqlSelect = "SELECT * FROM %s" % (tableSelect)
    viewTable = execute_read_query(conn, sqlSelect)
    return jsonify(viewTable)

# Add to inventory table in database
@app.route('/api/add_inventory', methods=['POST'])
def addInven():
    category = request.json.get("category")
    item = request.json.get("item")
    price = request.json.get("price")

    post_statement = "INSERT INTO inventory (category, item, price) VALUES ('%s','%s','%s')" % (category, item, price)
    execute_query(conn, post_statement)
    return "Successfully added!"


app.run()