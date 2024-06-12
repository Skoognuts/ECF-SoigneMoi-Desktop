#-*- coding: utf-8 -*-

import bcrypt
import mysql.connector

def checkCredentials(username, password):
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            database = "soigne_moi",
            user = "root",
            password = ""
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM user")
        users = mycursor.fetchall()
        for user in users:
            if username == user[1]:
                hashed = user[2].encode()
                bytes = password.encode()
                if bcrypt.checkpw(bytes, hashed):
                    return(True, user)
                else:
                    return(False, True)
        mydb.close()
    except:
        return(False, False)
