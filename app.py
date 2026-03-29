from flask import Flask, redirect, render_template, request, url_for
import mysql.connector

app = Flask(__name__)

# DB Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vishwa12@",
    database="campus_system"
)

cursor = db.cursor()

# LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ""
    success = ""
    role = ""

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        query = "SELECT * FROM USER WHERE Email=%s AND Password=%s AND Role=%s"
        cursor.execute(query, (email, password, role))
        user = cursor.fetchone()

        if user:
            success = "true"
        else:
            error = "Invalid Credentials"
            role = ""

    return render_template('login.html', error=error, success=success, role=role)


# DASHBOARDS
@app.route('/admin')
def admin_dashboard():
    return render_template('admin4.html')


@app.route('/user')
def user_dashboard():
    return render_template('user2.html')


# ✅ FIXED: THIS MUST BE ABOVE app.run()
@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    try:
        category = request.form['category']
        location = request.form['location']
        description = request.form['description']

        query = """
        INSERT INTO complaint (category, location, description, status)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (category, location, description, "Pending"))
        db.commit()

        return {"status": "success"}   # JSON response

    except Exception as e:
        print("ERROR:", e)
        return {"status": "error"}


# ✅ ALWAYS LAST
if __name__ == '__main__':
    app.run(debug=True)