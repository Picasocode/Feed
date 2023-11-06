from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import model as dbHandler
import sqlite3

app = Flask(__name__)
@app.route('/home')
def home():
       return render_template("index.html")
@app.route('/signup_api', methods=['POST', 'GET'])
def signup_api():
    if request.method=='POST':
           username = request.form['username']
           password = request.form['password']
           email=request.form['email']
           dbHandler.insertUser(username, password,email)
           return redirect("/")
    else:
           return render_template('error.html')

@app.route('/login_api', methods=['POST', 'GET'])
def login_api():
    if request.method=='POST':
           username = request.form['username']
           password = request.form['password']
           users=dbHandler.retrieveUsers()
           if (username,password) in users:
            return redirect('/home')
           else:
            return render_template('error.html')

@app.route('/')
def login():
       return render_template("login.html")

@app.route('/signup')
def signup():
       return render_template("signup.html")

@app.route('/logout')
def logout():
       return redirect('/')
@app.route('/request_form')
def request_form():
       return render_template('request.html')

@app.route('/request_food', methods=['GET', 'POST'])
def request_food():
    dbHandler.create_database()
    if request.method == 'POST':
        restaurant_name = request.form['restaurant_name']
        food_name = request.form['food_name']
        quantity = request.form['quantity']
        email = request.form['email']
        phone = request.form['phone']

        conn = sqlite3.connect('food.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO food (restaurant_name, food_name, quantity, email, phone) VALUES (?, ?, ?, ?, ?)',
                       (restaurant_name, food_name, quantity, email, phone))
        conn.commit()
        conn.close()

        return redirect(url_for('list_food'))

    return render_template('request.html')
@app.route("/list")
def list_re():
    return render_template("re_list.html")

@app.route('/food_list')
def list_food():
    conn = sqlite3.connect('food.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM food')
    food_data = cursor.fetchall()
    conn.close()

    return render_template('food_list.html', food_data=food_data)

@app.route('/ngo_requests', methods=['GET', 'POST'])
def ngo_request():
    if request.method == 'POST':
        ngo_name = request.form['ngo_name']
        contact_person = request.form['contact_person']
        email = request.form['email']
        phone = request.form['phone']
        food_items_needed = request.form['food_items']

        conn = sqlite3.connect('ngo.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ngo (ngo_name, contact_person, email, phone, food_items_needed) VALUES (?, ?, ?, ?, ?)',
                       (ngo_name, contact_person, email, phone, food_items_needed))
        conn.commit()
        conn.close()

        return redirect(url_for('list_ngo_requests'))

    return render_template('ngo_requests.html')

# Route to display NGO requests
@app.route('/ngo_list')
def list_ngo_requests():
    dbHandler.create_ngo_database()
    conn = sqlite3.connect('ngo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ngo')
    ngo_data = cursor.fetchall()
    conn.close()

    return render_template('ngo_list.html', ngo_data=ngo_data)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')