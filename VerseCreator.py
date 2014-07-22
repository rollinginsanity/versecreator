#This is a small application for creating fictional worlds in which stories can then be written.
#Author: Reece Payne
#License: TBD
import sqlite3
from flask import Flask
from flask import g
from flask import request
from flask import render_template
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

    c = get_db().cursor()
    c.execute('SELECT UserName, Pass FROM tblUser WHERE UserName = ? LIMIT 1',  [uname])
    user_info =  c.fetchone()
    password_stored = user_info[1]
#    if password_stored == password_submitted:
#        return "YAY!"
    return password_stored + " " + password_submitted
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
    return 'Hello World!'
    
@app.route('/login',  methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        return authenticate_user(request.form['UserName'], request.form['Pass'])
    elif request.method == "GET":
        return render_template('login.html')


    

if __name__ == '__main__':
    app.run(debug=True)
