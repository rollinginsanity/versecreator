#This is a small application for creating fictional worlds in which stories can then be written.
#Author: Reece Payne
#License: Do Whatever You Want, but there's no claim from me that it will work, or that this won't explode your computer and eat the souls of your unborn children.
import sqlite3
from flask import Flask
from flask import g
from flask import request
from flask import render_template
from flask import session, redirect, url_for

#all my fun functions. vc means VerseCreator
from vcfuncs import sanitise
import vcfuncs

app = Flask(__name__)

#Some vars, can probably change or be externalised into a file at some stage.
database_file = 'versecreator.db'
default_admin = 'admin'

#Setting up a function to talk to the DB.
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database_file)
    return db


#When a request is finished it also closes the database connection.
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('home.html',  title="Verse Creator Home")

#Todo, Security
#new_uname, the username submitted in the create user form.
#new_upass, the users new password.
@app.route('/newuser',  methods=['GET',  'POST'])
def newuser():
    if request.method == "POST":
        vcfuncs.new_user(get_db(), sanitise(request.form['UserName']), sanitise(request.form['Pass']), sanitise(request.form['Bio']), sanitise(request.form['FirstName']), sanitise(request.form['LastName']))
        return redirect(url_for('listusers'))
    elif request.method == "GET":
        return render_template("new_user.html",  title="Create A New User")
    else:
        return render_template("new_user.html",  title="Create A New User")

#Lists all users, currently temporary, might change.
@app.route('/listusers')
def list_users():
    c = get_db().cursor()
    c.execute("SELECT ID, UserName, FirstName, LastName, Bio FROM tblUser")
    userlist = c.fetchall()
    return render_template("list_users.html",title="List All Users",users=userlist)

#gname = group name
#gdesc = group desc
@app.route('/newgroup',  methods=['GET', 'POST'])
def newgroup():
    if request.method == "POST":
        vcfuncs.new_group(get_db(), sanitise(request.form['GroupName']), sanitise(request.form['Description']))
        return redirect(url_for('listgroups'))
    elif request.method == "GET":
        return render_template("new_group.html",  title="Create A New Group")
    else:
        return render_template("new_group.html",  title="Create A New Group")

@app.route('/listgroups')
def listgroups():
    grouplist = ""
    c = get_db().cursor()
    for group in c.execute("SELECT * FROM tblGroup"):
        grouplist += str(group[0])+" "+group[1]+" "+group[2]+"<br />"
    return grouplist

@app.route('/addgroupmembership',  methods=['GET', 'POST'])
def newgroupmembership():
    if request.method == "POST":
        if vcfuncs.new_group_membership(get_db(),  sanitise(request.form['GroupID']),  sanitise(request.form['UserID'])):
            return redirect(url_for('home'))
        #change this.
        return "lol"
    else:
        return render_template('new_group_membership.html',  title="Add A User to A Group")

@app.route('/login',  methods=['GET', 'POST'])
def login():
    #This will either display the login form to the users (GET method) or log in the user through args passed by the login
    #form (POST)
    if request.method == "POST":
        if vcfuncs.authenticate_user(get_db(), sanitise(request.form['UserName']), sanitise(request.form['Pass'])):
            session['username'] = request.form['UserName']
            session['logged_in'] = True
            session['user_id'] = vcfuncs.get_user_id(get_db(), session['username'])
            #There needs to be a better way to validate admin users, but for the minute this will work.
            if session['username'] == "admin":
              session['is_admin'] = True
            return redirect(url_for('home'))
        else:
            return "Incorrect Login Credentials"

    elif request.method == "GET":
        return render_template('login.html',  title="Login")

@app.route('/user/<userid>')
def view_user(userid):
  return render_template("view_user.html", title="View User", userinfo=vcfuncs.get_user_info(get_db(), userid))


#Log the user out.
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

#This is bad, it will need to go.
@app.route('/debug')
def debug():
  return render_template('debug.html')

#Just a test for the editor template, this will actually be called by other
#functions that specifiy the context of what is being edited. :)
@app.route('/edit')
def edit():
  return render_template('editor.html', title="Editor")

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #Here for demo purposes, needs to be set somewhere safer in the long term.

if __name__ == '__main__':
    app.run(debug=True)
