# The goal of this Flask app is to serve as an example API that only retrieves(GET) the latest
# data from an SQL Server Database table. The connection the the server is established using
# the pyodbc python library.
###

import flask
from flask import jsonify, make_response
import pyodbc
from flask_cors import CORS
import datetime

app = flask.Flask(__name__)
CORS(app)

# Connection string for an SQL Server DB. If using web services such as AWS or Azure,
# the connection string can be copy and pasted directly from the database's management page.
###
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=address,port;'
                        'Database=xxx;'
                        'Uid=xxx;'
                        'Pwd=xxx;'
                        'Encrypt=yes;'
                        'TrustServerCertificate=no;'
                        'Connection Timeout=30;')



def retrieveLatest(days):
    date = datetime.datetime.today() - datetime.timedelta(days)
    cursor = conn.cursor()
    if date.month < 10:
        monthFormatted = f'0{date.month}'
        dateFormatted = "{}-{}-{}".format(date.year,monthFormatted,date.day)
    else:
        dateFormatted = "{}-{}-{}".format(date.year,date.month,date.day)

    cursor = conn.cursor()

    # Please note that the database table reference here serves as an example
    cursor.execute(f"SELECT * FROM DatabaseNameOnServer.dbo.TableName where Date= '{dateFormatted}'") 

    return cursor

# Returns rows from a table where Date equals the current date, or calls retrieveLatest to return
# the rows with the most recent date.
###
@app.route('/stock-info/', methods=['GET'])
def get_list():
    
    todaysList = retrieveLatest(0)
    daysToSubtract = 0
    while todaysList.rowcount == 0:
        daysToSubtract += 1
        todaysList = retrieveLatest(daysToSubtract)

    response = []
    columns = [column[0] for column in todaysList.description]
    for row in todaysList.fetchall():
        response.append(dict(zip(columns, row)))

    resp = make_response(jsonify(response)) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

# Returns all rows where a certain column has a value equivalent to <ticker>. In this case, we are
# returning a list of all rows in the table where the StockTicker column value equals <ticker>.
###
@app.route('/stock-info/<ticker>', methods=['GET'])
def get_history(ticker):
    cursor = conn.cursor()

    # Please note that the database table reference here serves as an example
    cursor.execute(f"SELECT * FROM DatabaseNameOnServer.dbo.TableName where StockTicker= '{ticker}' ")

    response = []
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        response.append(dict(zip(columns, row)))

    resp = make_response(jsonify(response)) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')