from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '63103453574bccae5541fa05'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(), unique = True, nullable = False)
    username = db.Column(db.String(), unique = False, nullable = False)
    password = db.Column(db.String(), nullable = False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            hash_object = hashlib.sha256(password.encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            if user.password == hex_dig:
                session['email'] = email
                return redirect(url_for('profile'))
        flash('Invalid email or password')
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists')
            return redirect(url_for('register'))
        elif password == confirm_password:
            hash_object = hashlib.sha256(password.encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            user = User(username=username, email=email, password=hex_dig)
            db.session.add(user)
            db.session.commit()
            session['email'] = email
            return redirect(url_for('profile'))
        else:
            flash('Passwords do not match')
            return redirect(url_for('register'))
    else:
        return render_template('login.html')
    
@app.route('/profile')
def profile():
    return render_template('profile.html')
if __name__ == '__main__':
    app.run(debug=True)