from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app =Flask(__name__)
mail=Mail(app)
s = URLSafeTimedSerializer('secret')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)



app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pinpoint.four.2020@gmail.com'
app.config['MAIL_PASSWORD'] = 'Google2020'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


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
    #admin_id=db.Column(db.Integer)

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


from random import seed
from random import randint
# seed random number generator
seed(1)
# generate some integers





@app.route('/add_admin', methods=["GET", "POST"])

def register():
    if request.method == "POST":
        uname = request.form['uname']
        email = request.form['mail']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']

        exists = Admin.query.filter_by(uname=uname).first()

        if not exists:
            register = Admin(uname = uname,fname=fname,lname=lname,mail = email, phone=phone)
            db.session.add(register)
            db.session.commit()
            
            v1 = randint(0, 1000)
            v2 = randint(0, 1000)
            psw=str(v1)+uname+str(v2)
            msg = Message('Welcome to Pinpoint Family', sender = 'pinpoint.four.2020@gmail.com', recipients = [email])
            msg.html = '<h5>Hi {}&emsp;{},</h5><h3>You are addded as admin at PINPOINT.<br>Please login PINPOINT using following details</h3><h5> Your Username : {} <br> Password : {}<br><br> Happy to connect with u <BR> Thank you<h5>'.format(fname,lname,uname,psw)

            mail.send(msg)

            
            flash('A new admin added successfullly','success')
            return render_template('add_admin.html')
        else:
            flash('Username already taken,try somethig else','error')

        
    return render_template('add_admin.html')
    

@app.route('/Users')
def remove():
    # Original query not typed due to un availabilty of tables...these are demo
    #result = Admin.execute("SELECT * FROM Admin")

    admin = Admin.query.all()

    normal= Admin.query.filter_by(uname='visddhya').all()
    
    third = Admin.query.filter_by(uname='vidhya123').all()

    officials = Admin.query.filter_by(uname='Suredfj123').all()
    officials = Admin.query.filter_by(uname='Suredfj123').all()
     #admin = Admin.query.all()

    #normal=Ordinary.query.all()
    
#third = Third.query.all()

    #officials = Authority.query.all()
    
    
    return render_template('remove.html', admin=admin,normal=normal,third=third, officials=officials)
 



@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Admin.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
   
    flash("User Deleted Successfully",'success')
    return redirect(url_for('remove'))
 
  




if(__name__ == "__main__"):
    db.create_all()
    app.run(debug=True)
    




