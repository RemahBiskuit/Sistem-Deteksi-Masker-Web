from flask import Flask, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = '$#a12sMGvA1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/sipemas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
Bootstrap = Bootstrap(app)

class Login(FlaskForm):
    username = StringField('', validators=[InputRequired()], render_kw={'autofocus':True, 'placeholder':'Username'})
    password = PasswordField('', validators=[InputRequired()], render_kw={'autofocus':True, 'placeholder':'Username'})
    level = SelectField('', validators=[InputRequired()], choices=[('Admin','Admin'), ('User','User')])

class User(db.Model) :
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.Text)
    id_role = db.Column(db.Integer)

    def __init__ (self,username,password,id_role):
        self.username = username
        if password != '':
            self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.id_role = id_role

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    nama_role = db.Column(db.String(100))

    def __init__(self,nama_role):
        self.nama_role = nama_role


@app.route('/')
def index():
    return redirect(url_for('login'))
def login_dulu(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login' in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrap
@app.route('/login')
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(user=form.username.data) .first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data) and user.level == form.level.data:
                session['login'] = True
                session['id'] = user.id
                session['level'] = user.level
                return redirect(url_for('dashboard'))
        pesan = "Username atau password anda salah"
        return render_template("login.html", pesan=pesan, form=form)
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
