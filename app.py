from flask import Flask ,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from wtforms import SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf.csrf import CSRFProtect




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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

    def __repr__(self):

        return '[Choice {}]'.format(self.dept)

def choice_query():
    return Third.query

class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label='dept')

@app.route('/select', methods=['GET', 'POST'])
def select():
    form = ChoiceForm()

    form.opts.query = Third.query.filter(Third.dept)

    if form.validate_on_submit():
        return '<html><h1>{}</h1></html>'.format(form.opts.data)

    return render_template('index.html', form=form)




    

@app.route('/admin')
def  dashboard():
    return render_template('dashboard.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/third_party')
def third():
    return render_template('add_third.html')

@app.route('/add_admin')
def admin():
    return render_template('add_admin.html')

@app.route('/remove_user')
def remove():
    return render_template('remove.html')

@app.route('/')
def init_db():
    

    # Create a test user
   # new_user = Third('Railway', 'Thrissur')
   
   ## db.session.commit()
    return render_template('table.html',value = Third.query.all())

if(__name__ == "__main__"):
    #db.create_all()
    app.run(debug=True)
    