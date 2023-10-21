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
@app.route('/api/login', methods=['POST'])
def usernamepw():
    # Get username/password from frontend
    authentication = request.get_json()

    # Set variables from frontend json
    username = authentication['username']
    password = authentication['password']
    # SHA256 Hash password
    hashedPassword = hashlib.sha256(password.encode()).hexdigest()

    # SQL Statement and execute with connection
    sqlStatement = f"SELECT * FROM users WHERE username='{username}' AND password='{hashedPassword}'"
    auth = execute_read_query(conn, sqlStatement)

    if auth:
        return 'SUCCESS!'
    else:
        return 'INVALID LOGIN'

# View table in database
@app.route('/overview', methods=['GET'])
def test_view():
    sqlStatement = "SELECT * FROM galloInventory"
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
    item = request.json.get("item")
    quantity = request.json.get("quantity")

    sqlStatement = "INSERT INTO sugarInventory (item, quantity) VALUES ('%s','%s')" % (item, quantity)
    execute_query(conn, sqlStatement)
    return "Successfully added!"

# Update to inventory table in database
@app.route('/api/update_inventory', methods=['POST'])
def updateInven():
    item = request.json.get("item")
    quantity = request.json.get("quantity")
# Not finished
    sqlStatement = "UPDATE sugarInventory SET category = '%s' WHERE id = CHANGEME" % (category)
    execute_query(conn, sqlStatement)
    return "Updated!"

# Delete from inventory table
@app.route('/api/del_inventory', methods=['DELETE'])
def delInven():
    category = request.json.get("category")

    sqlStatement = "DELETE FROM sugarInventory WHERE category = '%s'" % (category)
    execute_query(conn, sqlStatement)
    return "Deleted!"


app.run()

# References
# CIS3368 Code