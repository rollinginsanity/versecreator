#This file includes a number of misc functions that
#are used in the main application itself,  and really only
#relate to the app.
from cgi import escape
import hashlib

#BEGIN SECTION WHERE NEW STUFF IS CREATED, USERS, GROUPS, STORIES, THE LOT!
#A bunch of this will be stub functions for a bit.

#adds a user to a group within the database.
def new_group_membership(conn, group_id,  user_id):
    c = conn.cursor()
    c.execute("INSERT INTO tblGroupMemberShips(ID, GroupID, UserID) VALUES(null, ?, ?)", [group_id, user_id])
    conn.commit()
    return True

#creates new users.
def new_user(conn,  username,  password,  bio="Please write a bit about yourself",  fname="UNKNOWN",  lname="UNKNOWN"):
    c = conn.cursor()
    c.execute("INSERT INTO tblUSER VALUES(null, ?, ?, ?, ? ,?)",  [username, fname, lname, hash_pass(password), bio])
    conn.commit()
    return True

def new_group(conn, group_name, group_description):
    c = conn.cursor()
    c.execute("INSERT INTO tblGroup(ID, Name, Description) VALUES(null, ?, ?)",  [group_name, group_description])
    conn.commit()
    return True

#Verse/Story Related

def new_verse(title, user_name):
    #Will need to lookup the users username to get their ID as the query will need it as well as their first and last names.
    pass

def new_story():
    pass

def new_chapter():
    pass

#character Related

def new_character():
    pass

def new_character_relationship():
    pass

def new_character_verse_association():
    pass

def new_character_story_association():
    pass

def new_character_chapter_association():
    pass

def new_character_attribute():
    pass

def new_character_role_type():
    pass

def new_character_attribute_type():
    pass


#Cleans up user input by converting unicode to HTML entities.
def sanitise(text):
    return escape(text, quote=True)

#Authenticates the user.
#Takes a username and password entered in the login form and validates that the user exists before logging
#them in.
#TODO error throwing if a user doesn't exist.
def authenticate_user(conn,  uname,  password_submitted):
    #Getting the DB cursor
    c = conn.cursor()
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

#Gets a users ID for all sorts of relational awsomeness.
def get_user_id(conn, username):
  c = conn.cursor()
  c.execute('SELECT ID FROM tblUser WHERE UserName = ? LIMIT 1',  [username])
  id = c.fetchone()
  return id[0]

#Gets user information based off their ID
def get_user_info(conn, id):
  c = conn.cursor()
  c.execute('SELECT ID, UserName, FirstName, LastName, Bio FROM tblUser WHERE ID = ? LIMIT 1',  [id])
  return c.fetchone()

#This function hashes the submitted password.
def hash_pass(PassWord):
    password_encrypted = hashlib.sha256(PassWord.encode())
    return password_encrypted.hexdigest()
