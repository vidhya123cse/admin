from flask import Flask ,render_template
app = Flask(__name__)


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



if(__name__ == "__main__"):
    app.run(debug=True)