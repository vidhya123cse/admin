from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from random import seed
from random import randint
# seed random number generator
seed(1)
# generate some integers


app =Flask(__name__)
mail=Mail(app)
s = URLSafeTimedSerializer('secret')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
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


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, autoincrement=True)
    username = db.Column(db.String(50),unique=True, nullable=False,primary_key=True)
    password = db.Column(db.String(15),nullable=False)
    type = db.Column(db.String(15),nullable=False)

    def __init__(self,username,password,type):
        self.username=username
        self.password=password
        self.type=type
    
#Admin Table
class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    mail = db.Column(db.String(50))
    admin_id = db.Column(db.String(20))
    usr_name = db.Column(db.String, db.ForeignKey('User.username'),nullable=False)

    def __init__(self,usr_name,fname,lname,phone,mail,admin_id):
        self.usr_name=usr_name
        self.fname=fname
        self.lname=lname
        self.phone=phone
        self.mail=mail
        self.admin_id=admin_id 
        
#Authority Table
class Authority(db.Model):
    __tablename__ = 'Authority'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    phone = db.Column(db.Integer)
    mail = db.Column(db.String(50))
    job = db.Column(db.String(50))
    proof=db.Column(db.String(40))
    confirm=db.Column(db.Boolean,unique=False, default=False)
    usr_name = db.Column(db.String, db.ForeignKey('User.username'),nullable=False)
    

    def __init__(self,usr_name,fname,lname,phone,mail,job,proof,confirm):
        self.usr_name=usr_name
        self.fname=fname
        self.lname=lname
        self.phone=phone
        self.mail=mail
        self.job=job
        self.proof=proof 
        self.confirm=confirm


#Ordinary Table
class Ordinary(db.Model):
    __tablename__ = 'Ordinary'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    phone = db.Column(db.Integer)
    mail = db.Column(db.String(30))
    state = db.Column(db.String(30))
    city = db.Column(db.String(30))
    proof=db.Column(db.String(40))
    address=db.Column(db.String(50))
    zip = db.Column(db.Integer)
    confirm=db.Column(db.Boolean,unique=False, default=False)
    usr_name = db.Column(db.String, db.ForeignKey('User.username'),nullable=False)
    

    def __init__(self,usr_name,fname,lname,phone,mail,state,city,address,zip,proof,confirm):
        self.usr_name=usr_name
        self.fname=fname
        self.lname=lname
        self.phone=phone
        self.mail=mail
        self.state=state
        self.proof=proof    
        self.address=address
        self.city=city
        self.zip=zip
        self.confirm=confirm


#Other Table
class Other(db.Model):
    __tablename__ = 'Other'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    admin_approval = db.Column(db.String(5))
    admin_id =  db.Column(db.Integer)
    no_of_video_upload = db.Column(db.Integer)
    no_of_video_request = db.Column(db.Integer)
    third_party_issue_id = db.Column(db.Integer)
    third_party_pending_order = db.Column(db.String(10))
    third_party_response = db.Column(db.String(20))  #video available or not
    date= db.Column(db.String(20))
    start_time = db.Column(db.String(20))
    end_time = db.Column(db.String(20))
    live_recording_no=db.Column(db.Integer)
    usr_name = db.Column(db.String, db.ForeignKey('User.username'),nullable=False)
    

    def __init__(self,admin_approval,admin_id,no_of_video_upload,no_of_video_request,third_party_issue_id,third_party_pending_order,third_party_response,date,start_time,end_time,live_recording_no,usr_name):
        self.admin_approval=admin_approval
        self.admin_id=admin_id
        self.no_of_video_request=no_of_video_upload
        self.third_party_issue_id=third_party_issue_id
        self.third_party_pending_order=third_party_pending_order
        self.third_party_response=third_party_response
        self.date=date    
        self.start_time=start_time
        self.end_time=end_time
        self.live_recording_no=live_recording_no
        self.usr_name=usr_name


#Third table
class Third(db.Model):
    __tablename__ = 'Third'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    dept = db.Column(db.String(50))
    name = db.Column(db.String(50))
    mail = db.Column(db.String(50))
    third_party_id = db.Column(db.String(20))
    phone = db.Column(db.Integer)
    usr_name = db.Column(db.String, db.ForeignKey('User.username'),nullable=False)

    def __init__(self,usr_name,dept,name,mail,third_party_id,phone):
        self.usr_name=usr_name
        self.dept=dept
        self.name=name
        self.phone=phone
        self.mail=mail
        self.third_party_id=third_party_id


#Count table
class Count(db.Model):
    __tablename__ = 'Count'
    id = db.Column(db.Integer, primary_key=True)
    Ordinary = db.Column(db.Integer)
    Authority = db.Column(db.Integer)
    Admin = db.Column(db.Integer)
    Third_party = db.Column(db.Integer)
    Total_Real= db.Column(db.Integer)
    Total_upload = db.Column(db.Integer)
    Total_request = db.Column(db.Integer)

    def __init__(self,id,Ordinary,Authority,Admin,Third_party,Total_Real,Total_upload,Total_request):
        self.id = id
        self.Ordinary = Ordinary
        self.Authority = Authority
        self.Admin = Admin
        self.Third_party = Third_party
        self.Total_Real = Total_Real
        self.Total_upload = Total_upload
        self.Total_request = Total_request
        
#end

        




    

@app.route('/Admin')
def  dashboard():
    return render_template('dashboard.html')

@app.route('/Admin/user')
def user():
    return render_template('user.html')

@app.route('/Admin/third_party', methods=["GET","POST"])
def third():
     all = db.session.query(Third.dept.distinct()).all()
     len1 = len(all)
     
     #print(all)
     print(all[0])
     print(all[1])
     if request.method == "POST":
        dept = request.form['firstList']
        new = request.form['secondList']
        name = request.form['thirdList']
        phone = request.form['phone']
        mail1 = request.form['fourthList']
        if dept == 'Other':
            dept = new
        exists = Third.query.filter_by(mail = mail1).first()

        if not exists:
            
            v1 = randint(0, 1000)
            v2 = randint(0, 1000)
            value = Count.query.filter_by(id = 1).first()
            uname = dept + '_' + str(value.Third_party+1)
            third_party_id = uname
            psw=str(v1)+name+str(v2)
            

            user = User(username=uname,password=psw,type='Third_party')
            register = Third(usr_name = uname, dept=dept, name=name, mail = mail1, phone=phone, third_party_id = third_party_id)
            count = Count.query.filter_by(id = 1).first()
            count.Third_party = count.Third_party + 1
            db.session.add(user)
            db.session.add(register)
            db.session.add(count)
            db.session.commit()
            
            msg = Message('Welcome to Pinpoint Family', sender = 'pinpoint.four.2020@gmail.com', recipients = [mail1])
            msg.html = '<h5>Hi,</h5><h3>You are addded as Third Party at PINPOINT.<br>Please login PINPOINT using following details</h3><h5> Your Username : {} <br> Password : {}<br><br> Happy to connect with u <BR> Thank you<h5>'.format(uname,psw)

            mail.send(msg)


            
            flash('A new Third Party added successfullly','success')
            return render_template('add_third.html',all = all)
        else:
            flash('Already Registered','error')



     return render_template('add_third.html',all = all)








@app.route('/Admin/add_admin', methods=["GET","POST"])

def register():
    if request.method == "POST":
        uname = request.form['uname']
        email = request.form['mail']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']

        exists = User.query.filter_by(username = uname).first()

        if not exists:
            
            v1 = randint(0, 1000)
            v2 = randint(100, 999)
            psw=str(v1)+uname+str(v2)
            value = Count.query.filter_by(id = 1).first()
            admin_id = "Admin_" + str(value.Admin+1)

            user = User(username=uname,password=psw,type='Admin')
            register = Admin(usr_name = uname,fname=fname,lname=lname,mail = email, phone=phone, admin_id = admin_id)
            count = Count.query.filter_by(id = 1).first()
            count.Admin = count.Admin + 1
            db.session.add(user)
            db.session.add(register)
            db.session.add(count)
            db.session.commit()
            
            
            msg = Message('Welcome to Pinpoint Family', sender = 'pinpoint.four.2020@gmail.com', recipients = [email])
            msg.html = '<h5>Hi {}&emsp;{},</h5><h3>You are addded as admin at PINPOINT.<br>Please login PINPOINT using following details</h3><h5> Your Username : {} <br> Password : {}<br><br> Happy to connect with u <BR> Thank you<h5>'.format(fname,lname,uname,psw)

            mail.send(msg)

            
            flash('A new admin added successfullly','success')
            return render_template('add_admin.html')
        else:
            flash('Username already taken,try somethig else','error')

        
    return render_template('add_admin.html')
    

@app.route('/Admin/remove_user')
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
    app.run(debug=True)
    




