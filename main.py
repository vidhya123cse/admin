
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired





app = Flask(__name__)
app.config.from_pyfile('config.cfg')
mail = Mail(app)
s = URLSafeTimedSerializer('secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class Third(db.Model):
    __tablename__ = 'Third'
    id = db.Column(db.Integer, primary_key=True)
    dept = db.Column(db.String(50))
    city = db.Column(db.String(50))

    def __init__(self,dept,city):
        self.dept=dept
        self.city=city
class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(50))
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    mail = db.Column(db.String(50))

    def __init__(self,uname,fname,lname,phone,mail):
        self.uname=uname
        self.fname=fname
        self.lname=lname
        self.phone=phone
        self.mail=mail



    

@app.route('/admin')
def  dashboard():
    return render_template('dashboard.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/third_party')
def third():
    return render_template('add_third.html')

@app.route('/add_admin', methods=["GET", "POST"])

def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']

        register = Admin(uname = uname,fname=fname,lname=lname,mail = mail, phone=phone)
        db.session.add(register)
        db.session.commit()
        #msg = Message('Welcome to pinpoint Family', sender='pinpoint.four.2020@gmail.com', recipients=[mail])
       # psw=uname+phone
        #msg.body = '<h2>You are addded as admin successfully.Please login PIPPOINT using following details</h2><br>Your Username is {} and Password is {}'.format(uname,psw)
        mail.send(msg)

         msg = mail.send_message(
        'Send Mail tutorial!',
       sender='pinpoint.four.2020@gmail.com', recipients=[mail],
        body="Congratulations you've succeeded!"
    )

        flash('A new admin added successfullly')
        return render_template('add_admin.html')
        
    return render_template('add_admin.html')
    

@app.route('/remove_user')
def remove():
    return render_template('remove.html')



if(__name__ == "__main__"):
    db.create_all()
    app.run(debug=True)
    

