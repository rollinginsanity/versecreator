#Script from: http://stackoverflow.com/questions/2380553/sqlite-run-multi-line-sql-script-from-file - Dirk Bester
#Naturally delete this script once you have run it, otherwise someone who has access to the file system can re-create your DB
#or see what the default admin password is. I'll write some code later around password resets, and recommend you reset the password.
import sqlite3
import os
import os.path
import ctypes
import hashlib

databaseFile = 'versecreator.db'
sqlFile = 'versecreatorDB.sql'

# Delete the old table
if os.path.isfile(databaseFile):
    os.remove(databaseFile)

# Create the tables
qry = open(sqlFile, 'r').read()
sqlite3.complete_statement(qry)
conn = sqlite3.connect(databaseFile)
cursor = conn.cursor()
try:
    cursor.executescript(qry)
except Exception as e:
    MessageBoxW = ctypes.windll.user32.MessageBoxW
    errorMessage = databaseFile + ': ' + str(e)
    MessageBoxW(None, errorMessage, 'Error', 0)
    cursor.close()
    raise
    
#Add in the default username
username = "admin"

#If you're not in the know, the 'b' turns the string into bytes.
password = b"s3cret"

#Encrypting the admin password.
password_encrypted = hashlib.sha256(password)

#This is for the query below. The field order is UserName, FirstName, LastName, Pass, Bio
admininfo = ["admin", "Admin", "Istrator", password_encrypted.hexdigest(), "Blah"]

cursor.execute("INSERT INTO tblUSER(ID, UserName, FirstName, LastName, Pass, Bio) VALUES(null, ?, ?, ?, ?, ?)",  admininfo)


#Hey kids, always remember to commit before closing!
conn.commit()

conn.close()
