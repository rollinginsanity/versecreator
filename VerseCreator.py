#This is a small application for creating fictional worlds in which stories can then be written.
#Author: Reece Payne
#License: TBD
import sqlite3
from flask import Flask
from flask import g
from flask import request
from flask import render_template
from flask import session, redirect, url_for
import hashlib

app = Flask(__name__)

#Some vars, can probably change or be externalised into a file at some stage.
databaseFile = 'versecreator.db'

#Setting up a function to talk to the DB.
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(databaseFile)
    return db

#Authenticates the user.
#Takes a username and password entered in the login form and validates that the user exists before logging
#them in.
#TODO error throwing if a user doesn't exist.
def authenticate_user(uname,  password_submitted):
    #Getting the DB cursor
    c = get_db().cursor()
    #Getting username from the DB. Note the [], remember this function takes a tuple, not a single string.
    c.execute('SELECT UserName, Pass FROM tblUser WHERE UserName = ? LIMIT 1',  [uname])
    #One line returned, no need for a foreach.
    user_info = c.fetchone()
    #Checking to see if there was any user records returned.
    if not user_info:
        return False
    #Gets the password.
    password_stored = user_info[1]
    #compares the newly hashed submitted pass against the hash in the DB
    if password_stored == hash_pass(password_submitted):
        return True
    else:
        return False

    
#This function hashes the submitted password.
def hash_pass(PassWord):
    password_encrypted = hashlib.sha256(PassWord.encode())
    return password_encrypted.hexdigest()
    
#When a request is finished it also closes the database connection.
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def hello_world():
    if 'username' in session:
        return 'Hello ' + session['username']
    else:
        return 'Hello World!'
    
@app.route('/login',  methods=['GET', 'POST'])
def login():
    #This will either display the login form to the users (GET method) or log in the user through args passed by the login
    #form (POST)
    if request.method == "POST":
        if authenticate_user(request.form['UserName'], request.form['Pass']):
            session['username'] = request.form['UserName']
            return redirect(url_for('hello_world'))
        else:
            return "Incorrect Login Credentials"
        
    elif request.method == "GET":
        return render_template('login.html')
 
#Log the user out. 
@app.route('/logout')
def logout():
    session.pop('username',  None)
    return redirect(url_for('hello_world'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #Here for demo putposes, needs to be set somewhere safer in the long term.

if __name__ == '__main__':
    app.run(debug=True)
