#!/usr/bin/python3
from flask import request, render_template, Flask, jsonify, session
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb.cursors

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

@app.route('/delete/<int:item_id>', methods=['DELETE'])
def del_item(item_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM general WHERE item_id=%s', (item_id,))
        mysql.connection.commit()
        cur.close()

        return 'Item DELETED', 200

    except Exception as e:
        return str(e), 400


@app.route('/edit/<int:item_id>', methods=['PUT'])
def edit_item(item_id):
    try:
        data = request.get_json()
        name = data['itemName']
        quantity = data['itemQuantity']
        category = data['itemCategory']
        brand = data['itemBrand']
        notes = data['itemNotes']

        cur = mysql.connection.cursor()
        cur.execute('UPDATE general SET item_name=%s, item_quantity=%s, item_category=%s, brand=%s, notes=%s WHERE item_id=%s', (name, quantity, category, brand,notes, item_id))
        mysql.connection.commit()
        cur.close()

        return 'item UPDATED', 200

    except Exception as e:
        return str(e), 400

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM password WHERE username=%s AND password=%s', (username, password))
        account = cur.fetchone()
        cur.close()
        if account:
            session['loggedin'] = True
            session['id'] = account['pass_id']
            session['username'] = account['username']
            message = 'Logged in Succesfully'
            return render_template('home.html', message=message)
        else:
            message = 'Incorrect username/password'

    return render_template('login.html', message=message)


@app.route('/logout')
def logout():
    session.pop['loggedin', None]
    session.pop['id', None]
    session.pop['username', None]
    return render_template('login.html')

@app.route('/register')
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM password WHERE username=%s', (username, ))
        account = cur.fetchone()

        # check credibility of information filled
        if account:
            message = 'Account already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cur.execute('INSERT INTO password(username, password, email) VALUES (%s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            cur.close()
            message = 'Logged in successfully'
    
    elif request.method == 'POST':
        message = 'Please fill the form'
    
    return render_template('register.html', message=message)



if  __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
