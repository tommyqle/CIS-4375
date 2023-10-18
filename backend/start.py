# Before first run do:
# pip install mysql.connector
# pip install npm
# npm install flask
# Run by:
# python start.py

import creds
import flask
import hashlib
import json
from flask import request, make_response, jsonify
from sql import create_connection, execute_query, execute_read_query

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create connection to MySQL database
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

# Login with Password
@app.route('/api/login', methods=['GET'])
def usernamepw():
    # SQL query to put all users in a list
    sqlStatement = "SELECT * FROM users"
    authorizedusers = execute_read_query(conn, sqlStatement)

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
    sqlStatement = "SELECT * FROM inventory"
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)

# View table in database
@app.route('/overview', methods=['GET'])
def test_view():
    tableSelect = "inventory"
    sqlStatement = "SELECT * FROM %s" % (tableSelect)
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)

# Tommy - testing sugarland inventory view table
@app.route('/sugarland', methods=['GET'])
def view_sugarland_inv():
    tableSelect = "sugarInventory"
    sqlStatement = "SELECT * FROM %s" % (tableSelect)
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)

# Tommy - testing Galleria inventory view table
@app.route('/galleria', methods=['GET'])
def view_galleria_inv():
    tableSelect = "galloInventory"
    sqlStatement = "SELECT * FROM %s" % (tableSelect)
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)

# Add to inventory table in database
@app.route('/api/add_inventory', methods=['POST'])
def addInven():
    category = request.json.get("category")
    item = request.json.get("item")
    price = request.json.get("price")

    sqlStatement = "INSERT INTO inventory (category, item, price) VALUES ('%s','%s','%s')" % (category, item, price)
    execute_query(conn, sqlStatement)
    return "Successfully added!"

# Update to inventory table in database
@app.route('/api/update_inventory', methods=['POST'])
def updateInven():
    category = request.json.get("category")
    item = request.json.get("item")
    price = request.json.get("price")
# Not finished
    sqlStatement = "UPDATE inventory SET category = '%s' WHERE id = CHANGEME" % (category)
    execute_query(conn, sqlStatement)
    return "Updated!"

# Delete from inventory table
@app.route('/api/del_inventory', methods=['DELETE'])
def delInven():
    category = request.json.get("category")

    sqlStatement = "DELETE FROM inventory WHERE category = '%s'" % (category)
    execute_query(conn, sqlStatement)
    return "Deleted!"


app.run()

# References
# CIS3368 Code