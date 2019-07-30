from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, ConnectForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b3089f8f11c5d7ee024127f21a2502d6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date}')"

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/user/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}', 'success')
		return redirect(url_for('/user/login'))
	return render_template('register.html', title='Register', form=form)
	
@app.route('/user/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.username.data == 'admin' and form.password.data == 'password':
			flash(f'You have been logged in', 'success')
			return redirect(url_for('home'))
		else:
			flash(f'Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/user')
def user():
    return render_template('user.html', title='User')
	
@app.route('/user/view')
def view():
    return render_template('view.html', title='View')

@app.route('/user/view/client')
def client():
    return render_template('client.html', title='Client')

@app.route('/user/connect', methods=['GET', 'POST'])
def connect():
	form = ConnectForm()
	if form.validate_on_submit():
		flash(f'Connected', 'success')
		return redirect(url_for('connect'))
	return render_template('connect.html', title='Connect', form=form)

@app.route('/user/connect/interact')
def interact():
    return render_template('interact.html', title='Interact')

@app.route('/user/define')
def define():
    return render_template('define.html', title='Define')
	
if __name__ == "__main__":
	app.run(debug=True)