import flask
import json
from flask import request, make_response
from sql import create_connection, execute_query, execute_read_query
import creds

# Before first run do:
# pip install mysql.connector
# pip install npm
# npm install flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create connection to MySQL database
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

# Test input data to database
testData = [
    {"name": "Hussain"}
]

@app.route('/api/test', methods=['POST'])
def testAdd():
    test_dict = json.load(testData)
    newName = test_dict['name']

    post_statement = "INSERT INTO test (name) VALUES ('%s')" % (newName)
    execute_query(conn, post_statement)
    return "Successfully added!"












app.run()