from flask import Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'review_database'
mysql = MySQL(app)

#home
@app.route('/')
def home():
    return render_template('home.html')

#user signup view

@app.route('/user_signup', methods = ['POST', 'GET'])
def user_signup():
    if request.method == 'GET':
        return render_template('user_signup.html')

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(first_name, last_name, email, hash_password)VALUES (%s, %s, %s, %s)",(first_name, last_name, email, hash_password))
        mysql.connection.commit()
        return redirect(url_for('home')) # change the url to restaurant view when done. 


#user login view

@app.route('/user_login', methods= ['POST', 'GET'])
def user_login():
    if request.method == 'GET':
        return render_template('user_login.html')
    elif request.method == 'POST':
        email = request.form['email']
        print(email)
        password = request.form['password'].encode('utf-8')
        print(password)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        print(user)
        if len(user) > 0:
            if bcrypt.hashpw(password, user[4].encode('utf-8')) == user[4].encode('utf-8'):
                session['user_id'] = user[0]
                print(session['user_id'])
                session['first_name'] = user[1]
                session['email'] = user[3]
                return redirect(url_for('restaurant_view_user')) # render the needed view function here
            else:
                return render_template('user_login.html') #use flash message("Error password and email not match")
        else:
            return render_template('user_login.html')# use flash message("Error user not found")
    else:
        return render_template('user_login.html') #use flash message(please log in) 


#admin signup view

@app.route('/admin_signup', methods = ['GET','POST'])
def admin_signup():
    if request.method == 'GET':
        return render_template('admin_signup.html')
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO admin(first_name, last_name, email, hash_password)VALUES (%s, %s, %s, %s)",(first_name, last_name, email, hash_password))
        mysql.connection.commit()
        return redirect(url_for('home')) # change the url to restaurant view when done.


#admin login view

@app.route('/admin_login', methods= ['POST', 'GET'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')
    elif request.method == 'POST':
        email = request.form['email']
        print(email)
        password = request.form['password'].encode('utf-8')
        print(password)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin WHERE email = %s", (email,))
        user = cur.fetchone()
        print(user)
        if len(user) > 0:
            if bcrypt.hashpw(password, user[4].encode('utf-8')) == user[4].encode('utf-8'):
                session['admin_id'] = user[0]
                session['first_name'] = user[1]
                session['email'] = user[3]
                return redirect(url_for('restaurant_view')) # render the needed view function here
            else:
                return render_template('admin_login.html') #use flash message("Error password and email not match")
        else:
            return render_template('admin_login.html')# use flash message("Error user not found")
    else:
        return render_template('admin_login.html') #use flash message(please log in) 
    

#Read View restaurant for admin

@app.route('/restaurant_view')
def restaurant_view():
    if 'admin_id' in session:
        cur = mysql.connection.cursor()
        Q1 = "SELECT * FROM restaurants"
        cur.execute(Q1)
        data = cur.fetchall()
        return render_template('restaurant_view.html', restaurants = data, admin_id = session['admin_id'])
    else:
        return "Please log in first"

#Insert View Restaurant only for admin

@app.route('/insert_restaurant', methods= ['GET', 'POST'])
def insert_restaurant():
    if 'admin_id' in session:
        if request.method == 'POST':
            name = request.form['name']
            address = request.form['address']
            phone = request.form['phone']
            admin_id = request.form['admin_id']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO restaurants(name,address,phone, admin_id)VALUES (%s, %s, %s, %s)",(name, address, phone, admin_id))
            mysql.connection.commit()
            return redirect(url_for('restaurant_view'))
    else:
        return "Please log in first"

#Delete View Restaurant only for admin

@app.route('/delete_restaurant/<int:id>', methods = ['GET', 'POST'])
def delete_restaurant(id):
    Id = id
    if 'admin_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT admin_id FROM restaurants WHERE id = %s", (Id,))
        data = cur.fetchone()
        if data[0] == session['admin_id']:
            if request.method == 'GET':
                return render_template('delete_restaurant.html', Id= id)
    
            if request.method == 'POST':
                Id = request.form['Id']
                cur = mysql.connection.cursor() 
                cur.execute("DELETE FROM restaurants WHERE id = %s", (Id,))
                mysql.connection.commit()
                return redirect(url_for('restaurant_view'))
        else:
            return "you can not delete this restaurant"
    else:
        return "Please log in first"

#update view restaurant

@app.route('/update_restaurant/<int:id>', methods = ['GET', 'POST'])
def update_restaurant(id):
    Id = id
    if 'admin_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT admin_id FROM restaurants WHERE id = %s", (Id,))
        data = cur.fetchone()
        if data[0] == session['admin_id']:
            if request.method == 'GET':
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM restaurants WHERE id = %s", (Id,))
                data = cur.fetchone()
                return render_template('update_restaurant.html', name= data[1],address = data[2], phone = data[3], Id = data[0])
            elif request.method == 'POST':
                Id = request.form['Id']
                name = request.form['name']
                address = request.form['address']
                phone = request.form['phone']
                cur = mysql.connection.cursor()
                Q4 = "UPDATE restaurants SET name=%s,address=%s, phone=%s WHERE id = %s"""
                V1 = (name,address, phone, Id)
                cur.execute(Q4,V1)
                mysql.connection.commit()
                return redirect(url_for('restaurant_view'))
        else:
            return "you can not edit this data"
    else:
        return "Please log in first"


#check Review restaurant for admin

@app.route('/check_review/<int:id>')
def check_review(id):
    Id = id
    if 'admin_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM reviews WHERE review_id = %s", (Id,))
        data = cur.fetchall()
        return render_template('check_review.html', reviews = data, Id = Id)
    elif 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM reviews WHERE review_id = %s", (Id,))
        data = cur.fetchall()
        return render_template('check_review.html', reviews = data, Id = Id, user_id = session['user_id'])
    else:
        return "Please log in first"

#read view restaurant for user

@app.route('/restaurant_view_user')
def restaurant_view_user():
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        Q1 = "SELECT * FROM restaurants"
        cur.execute(Q1)
        data = cur.fetchall()
        return render_template('restaurant_view_user.html', restaurants = data)
    else:
        return "Please log in first"

#insert a review from user

@app.route('/insert_review', methods= ['GET', 'POST'])
def insert_review():
    if 'user_id' in session:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            age = request.form['age']
            address = request.form['address']
            rating = request.form['rating']
            description = request.form['description']
            review_id = request.form['review_id']
            user_id = request.form['user_id']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO reviews(name, email, age, address, rating, description, review_id, user_id)VALUES (%s, %s, %s, %s, %s, %s,%s, %s)",(name, email, age, address, rating, description, review_id, user_id))
            mysql.connection.commit()
            return redirect(url_for('restaurant_view_user'))
    else:
        return "Please log in first"

#delete review by user


@app.route('/delete_review/<int:id>', methods = ['GET', 'POST'])
def delete_review(id):
    Id = id
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id FROM reviews WHERE id = %s", (Id,))
        data = cur.fetchone()
        if data[0] == session['user_id']:
            if request.method == 'GET':
                return render_template('delete_review.html', Id= id)
            if request.method == 'POST':
                Id = request.form['Id']
                cur = mysql.connection.cursor()
                Q2 = "DELETE FROM reviews WHERE id = %s"
                V = (Id,)
                cur.execute(Q2,V)
                mysql.connection.commit()
                return redirect(url_for('restaurant_view_user'))
        else:
            return "sorry, you can not delete this review"
    else:
        return "Please log in first"


#update view review by user

@app.route('/update_review/<int:id>', methods = ['GET', 'POST'])
def update_review(id):
    Id = id
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id FROM reviews WHERE id = %s", (Id,))
        data = cur.fetchone()
        print('data=', data)
        if data[0] == session['user_id']:
            if request.method == 'GET':
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM reviews WHERE id = %s", (Id,))
                data = cur.fetchone()
                return render_template('update_review.html', name= data[1],email = data[2],age = data[3],address = data[4],rating = data[5],description=data[6], Id = data[0])
            if request.method == 'POST':
                Id = request.form['Id']
                name = request.form['name']
                email = request.form['email']
                age = request.form['age']
                address = request.form['address']
                rating = request.form['rating']
                description = request.form['description']
                cur = mysql.connection.cursor()
                Q4 = "UPDATE reviews SET name=%s, email=%s, age=%s, address=%s, rating=%s,description=%s WHERE id = %s"""
                V1 = (name, email, age, address, rating,description, Id)
                cur.execute(Q4,V1)
                mysql.connection.commit()
                return redirect(url_for('restaurant_view_user'))
        else:
            return "sorry, you can not update this review"
    else:
        return "Please log in first"


@app.route('/logout', methods=["GET", "POST"])
def logout():
    if 'admin_id' in session:
        session.clear()
        return render_template("home.html")
    elif 'user_id' in session:
        session.clear()
        return render_template("home.html")
    else:
        return "Please log in first"






if __name__ == '__main__':
    app.secret_key = "mitu"
    app.run(debug=True)
