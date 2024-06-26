#!/usr/bin/python3
from flask import request, render_template, Flask, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL

# Creating Flask app
app = Flask(__name__)

# To allow front end to interact with backend
CORS(app)

# Configurations of MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PASSWORD'] = 'Peterodero561@'
app.config['MYSQL_DB'] = 'inventory'

mysql = MySQL(app)

@app.route('/add', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        name = data['itemName']
        quantity = data['itemQuantity']
        category = data['itemCategory']
        brand = data['itemBrand']
        notes = data['itemNotes']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO general (item_name, item_quantity, item_category, brand, notes) VALUES (%s, %s, %s, %s, %s)', (name, quantity, category, brand, notes))
        mysql.connection.commit()
        cur.close()

        return 'Item added', 200
    except Exception as e:
        return str(e), 400

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/stock', methods=['GET'])
def get_stock():
    # getting the data stored in the Inventory database in general table
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM general')
    results = cur.fetchall()
    cur.close()

    # arranging the results
    stocks = []
    for row in results:
        stock = {
                'item_id': row[0],
                'itemName': row[1],
                'itemQuantity': row[2],
                'itemCategory': row[3],
                'itemBrand': row[4],
                'itemNotes': row[5]
                }
        stocks.append(stock)

    return jsonify(stocks), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
