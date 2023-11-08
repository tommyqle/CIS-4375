# Before first run do:
# pip install mysql.connector
# pip install npm
# pip install flask-cors
# npm install flask
# Run by:
# python start.py

import parameters
import flask
import hashlib
from flask import request, jsonify
from flask_cors import CORS
from sql import create_connection, execute_query, execute_read_query

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

# Create connection to MySQL database
myCreds = parameters.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
myTables = parameters.Tables()

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
    sqlStatement = f"SELECT * FROM {myTables.users} WHERE username='{username}' AND password='{hashedPassword}'"
    auth = execute_read_query(conn, sqlStatement)

    if auth:
        return 'SUCCESS!'
    else:
        return 'INVALID LOGIN'

# ========================= View Pages =========================
# Sugar Land inventory view
@app.route('/sugarland', methods=['GET'])
def view_sugarland_inv():
    # Select * from sugarInventory table and make all caps
    sqlStatement = f"SELECT id, UPPER(item) AS item, UPPER(category) AS category, quantity, price FROM {myTables.sugarland};"
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)

# Galleria inventory view - copy of /sugarland
@app.route('/galleria', methods=['GET'])
def view_galleria_inv():
    sqlStatement = f"SELECT id, UPPER(item) AS item, UPPER(category) AS category, quantity, price FROM {myTables.galleria};"
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)

# Product view for editing inventory
@app.route('/edit_inv', methods=['GET'])
def view_product_inv():
    sqlStatement = f"SELECT * FROM {myTables.product}"
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)
# ========================= View Pages =========================

# ============================ CRUD =============================
# Add to product table in database
@app.route('/api/add_inventory', methods=['POST'])
def addProdInven():
    category = request.json.get("category")
    item = request.json.get("itemName")
    price = request.json.get("price")

    # Insert new entry based on user-inputted values
    sqlStatement = f"INSERT INTO {myTables.product} (category_name, product_name, price) VALUES ('%s','%s','%s')" % (category, item, price)
    execute_query(conn, sqlStatement)
    return "Successfully added!"

# Delete from product table in database
@app.route('/api/del_inventory', methods=['DELETE'])
def delProdInven():
    item = request.json.get("itemName")
    
    # Delete entry solely from item name
    sqlStatement = f"SELECT product_id FROM {myTables.product} WHERE product_name = '%s'" % (item)
    productID = execute_read_query(conn, sqlStatement)
    
    # Check if item name exists
    if productID:
        if len(productID) > 0:
            productID = productID[0]['product_id']
            sqlStatement = f"DELETE FROM {myTables.product} WHERE product_id = '%s'" % (productID)
            execute_query(conn, sqlStatement)
            return "Successfully deleted!"
        else:
            return jsonify({"message": "No Item ID found."}), 404
    else:
        return jsonify({"message": "No Item ID found."}), 404

# Update to inventory table in database
@app.route('/api/update_inventory', methods=['POST'])
def updateInven():
    updateItem = request.json.get("updateItem")
    category = request.json.get("category")
    item = request.json.get("itemName")
    price = request.json.get("price")

    # Get id by using item name
    sqlStatement = f"SELECT product_id FROM {myTables.product} WHERE product_name = '%s'" % (updateItem)
    productID = execute_read_query(conn, sqlStatement)
    productID = productID[0]['product_id']

    # Update entry with grabbed id based on users inputted item name
    sqlStatement = f"UPDATE {myTables.product} SET category_name='%s',product_name='%s',price='%s' WHERE product_id='%s'" % (category,item,price,productID)
    execute_query(conn, sqlStatement)
    return "Successfully updated!"

# Update to tables quantity
@app.route('/api/update_quantity', methods=['POST'])
def updateQuant():
    origQuantities = request.json.get("origQuantities")
    quantities = request.json.get("quantity")
    ids = request.json.get("id")
    table = request.json.get("table")
    
    # for loop using the sequential id, quantity, origQuantity in each iteration
    for id, quantity, origQuantity in zip(ids, quantities, origQuantities):
        # If no change between quantities, do nothing
        if origQuantity == quantity:
            continue
        # Update quantity through SQL if quantity is changed (per item-based)
        else:
            sqlStatement = "UPDATE %s SET quantity='%s' WHERE id='%s'" % (table, quantity, id)
            execute_query(conn, sqlStatement)
    return "Successfully updated!"

# ============================ CRUD =============================


app.run()

"""
References
    CIS3368 Code
    CIS4339 Code (pulled ideas from code)
    https://www.w3resource.com/mysql/update-table/update-table.php
    https://realpython.com/python-zip-function/#looping-over-multiple-iterables
"""
