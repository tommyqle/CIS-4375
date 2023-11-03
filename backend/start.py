# Before first run do:
# pip install mysql.connector
# pip install npm
# pip install flask-cors
# npm install flask
# Run by:
# python start.py

import creds
import flask
import hashlib
import json
from flask import request, make_response, jsonify
from flask_cors import CORS
from sql import create_connection, execute_query, execute_read_query

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

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

# ========================= View Tables =========================
# View table in database
@app.route('/overview', methods=['GET'])
def test_view():
    sqlStatement = "SELECT * FROM product"
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)

# Tommy - testing sugarland inventory view table
@app.route('/sugarland', methods=['GET'])
def view_sugarland_inv():
    sqlStatement = "SELECT * FROM sugarInventory"
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)

# Tommy - testing Galleria inventory view table
@app.route('/galleria', methods=['GET'])
def view_galleria_inv():
    sqlStatement = "SELECT * FROM galloInventory"
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)

# Tommy - testing Edit Inventory view table
@app.route('/edit_inv', methods=['GET'])
def view_product_inv():
    sqlStatement = "SELECT * FROM product"
    viewTable = execute_read_query(conn, sqlStatement)
    return jsonify(viewTable)
# ========================= View Tables =========================

# ============================ CRUD =============================
# Add to product table in database
@app.route('/api/add_inventory', methods=['POST'])
def addProdInven():
    category = request.json.get("category")
    item = request.json.get("itemName")
    price = request.json.get("price")

    sqlStatement = "INSERT INTO product (category_name, product_name, price) VALUES ('%s','%s','%s')" % (category, item, price)
    execute_query(conn, sqlStatement)
    return "Successfully added!"

# Delete from product table in database
@app.route('/api/del_inventory', methods=['DELETE'])
def delProdInven():
    item = request.json.get("itemName")

    sqlStatement = "SELECT product_id FROM product WHERE product_name = '%s'" % (item)
    productID = execute_read_query(conn, sqlStatement)
    productID = productID[0]['product_id']

    if productID:
        sqlStatement = "DELETE FROM product WHERE product_id = '%s'" % (productID)
        execute_query(conn, sqlStatement)
        return "Successfully deleted!"
    else:
        return "No productID found."

# Update to inventory table in database
@app.route('/api/update_inventory', methods=['POST'])
def updateInven():
    updateItem = request.json.get("updateItem")
    category = request.json.get("category")
    item = request.json.get("itemName")
    price = request.json.get("price")

    sqlStatement = "SELECT product_id FROM product WHERE product_name = '%s'" % (updateItem)
    productID = execute_read_query(conn, sqlStatement)
    productID = productID[0]['product_id']

    sqlStatement = "UPDATE product SET category_name='%s',product_name='%s',price='%s' WHERE product_id='%s'" % (category,item,price,productID)
    execute_query(conn, sqlStatement)
    return "Successfully updated!"
# ============================ CRUD =============================


app.run()

# References
# CIS3368 Code
# https://www.w3resource.com/mysql/update-table/update-table.php