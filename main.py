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

class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable = False)
    holder = db.Column(db.String(), nullable = False)
    code = db.Column(db.String(), nullable = False)

class Temperature(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    serial_number = db.Column(db.String(), nullable = False)
    temp = db.Column(db.String(), nullable = False)
    humidity = db.Column(db.String(), nullable = False)

class Example(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(), nullable = False)

@app.route('/')
def home():
        
    
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'remember' in session and session['remember'] == True:
        return redirect(url_for('buttons'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            hash_object = hashlib.sha256(password.encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            if user.password == hex_dig:
                session['remember'] = True
                session['email'] = email
                session.permanent = True
                return redirect(url_for('buttons'))
        flash('Invalid email or password')
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'remember' in session and session['remember'] == True:
        return redirect(url_for('buttons'))

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
            session['remember'] = True
            session.permanent = True
            return redirect(url_for('buttons'))
        else:
            flash('Passwords do not match')
            return redirect(url_for('register'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop("email", None)
    session.pop("remember", None)
    return redirect('/')


@app.route('/profile', methods=["POST", "GET"])
def buttons():
    show = False
    if request.method == "POST":
        if "device" in request.form:
            show = True
        elif "hide" in request.form:
            show = False
    holder = session['email']
    codes = Code.query.filter_by(holder=holder).all()
    return render_template('profile.html', show=show, codes = codes)

@app.route('/code', methods=["POST", "GET"])
def thermometers():
    if request.method == "POST":
        code = request.form.get('code')
        if code == "":
            return redirect(url_for('buttons'))

        holder = session['email']
        name = request.form.get("name")
        if name == "":
            return redirect(url_for('buttons'))
        user = Code(name=name,code=code, holder=holder)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('buttons'))
    return render_template('profile.html')


@app.route('/data', methods=['POST'])
def save_data():
    # Code to save data to the database
    serial_number = request.form['serial_number']
    temp = request.form['temp']
    humidity = request.form['humidity']
    device = Temperature.query.filter_by(serial_number=serial_number).first()
    if device:
        device.temp = temp
        device.humidity = humidity
    else:
        device = Temperature(serial_number=serial_number, temp=temp, humidity=humidity)
        db.session.add(device)
    db.session.commit()
    return 'Data saved successfully!'

@app.route('/temp/<int:code_id>')
def temp(code_id):
    codes = Code.query.get_or_404(code_id)
    code = codes.code
    device = Temperature.query.filter_by(serial_number=code).first()
    if device is not None:
        temp = device.temp
        humidity = device.humidity
        full = Code.query.filter_by(code=code).first()
        name = full.name
        return render_template('temp.html', temp=temp, humidity=humidity, code=code, name=name)
    return render_template('temp.html', code=code)
if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)