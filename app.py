#!/usr/bin/python3
from flask import request, render_template, Flask, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

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

# secret key for creating unique sessions
app.secret_key = '1234'


@app.route('/add/<string:table_name>', methods=['POST'])
def add_item(table_name='ict'):
    try:
        # Validate table name to prevent SQL errors
        if table_name not in ['ict', 'furniture', 'attractive', 'vehicle']:
            return 'Invalid table name', 400
        
        data = request.get_json()
        name = data['itemName']
        quantity = data['itemQuantity']
        category = data['itemCategory']
        brand = data['itemBrand']
        notes = data['itemNotes']

        cur = mysql.connection.cursor()
        query = f'INSERT INTO {table_name} (item_name, item_quantity, item_category, brand, notes) VALUES (%s, %s, %s, %s, %s)'
        cur.execute(query, (name, quantity, category, brand, notes))
        mysql.connection.commit()
        cur.close()

        return 'Item added', 200
    except Exception as e:
        return str(e), 400


@app.route('/stock/<string:table_name>', methods=['GET'])
def get_stock(table_name):
    try:
        # Validate table name to prevent SQL errors
        if table_name not in ['ict', 'furniture', 'attractive', 'vehicle']:
            return 'Invalid table name', 400
        
        # getting the data stored in the Inventory database in the specified table
        cur = mysql.connection.cursor()
        query = f'SELECT * FROM {table_name}'
        cur.execute(query)
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

    except Exception as e:
        return str(e), 400

@app.route('/delete/<string:table_name>/<int:item_id>', methods=['DELETE'])
def del_item(table_name, item_id):
    try:
        # Validate table name to prevent SQL errors
        if table_name not in ['ict', 'furniture', 'attractive', 'vehicle']:
            return 'Invalid table name', 400
        
        cur = mysql.connection.cursor()
        query = f'DELETE FROM {table_name} WHERE item_id=%s'
        cur.execute(query, (item_id,))
        mysql.connection.commit()
        cur.close()

        return 'Item DELETED', 200

    except Exception as e:
        return str(e), 400


@app.route('/edit/<string:table_name>/<int:item_id>', methods=['PUT'])
def edit_item(table_name, item_id):
    try:
        data = request.get_json()
        name = data['itemName']
        quantity = data['itemQuantity']
        category = data['itemCategory']
        brand = data['itemBrand']
        notes = data['itemNotes']

        cur = mysql.connection.cursor()
        query = f'UPDATE {table_name} SET item_name=%s, item_quantity=%s, item_category=%s, brand=%s, notes=%s WHERE item_id=%s'
        cur.execute(query, (name, quantity, category, brand,notes, item_id))
        mysql.connection.commit()
        cur.close()

        return 'item UPDATED', 200

    except Exception as e:
        return str(e), 400

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM users WHERE email=%s AND password=%s', (email, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['email'] = user['email']
            message = 'Logged in Succesfully'
            if user['email'] == 'peterodero561@gmail.com' or user['email'] == 'dorwinogollao6@gmail.com':
                return render_template('home.html', message=message)
            else:
                return render_template('home2.html', message=message)
        else:
            message = 'Incorrect username/password'

    return render_template('signin.html', message=message)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    message = ''
    if request.method == 'POST' and 'fullname' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['fullname']
        password = request.form['password']
        email = request.form['email']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM users WHERE email=%s', (email, ))
        user = cur.fetchone()

        # check credibility of information filled
        if user:
            message = 'Account already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', fullname):
            msg = 'Username must contain only characters and numbers !'
        elif not fullname or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cur.execute('INSERT INTO users (full_name, password, email) VALUES (%s, %s, %s)', (fullname, password, email))
            mysql.connection.commit()
            cur.close()
            message = 'Signed up successfully. Proceed to Sign In'
    
    elif request.method == 'POST':
        message = 'Please fill the form'
    
    return render_template('signup.html', message=message)



if  __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
