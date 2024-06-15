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
        mydb.close()
        for user in users:
            if username == user[2]:
                if "ROLE_SECRETARY" in user[4]:
                    hashed = user[3].encode()
                    bytes = password.encode()
                    if bcrypt.checkpw(bytes, hashed):
                        return(True, user)
                    else:
                        return(False, True)
                else:
                    return(False, True)
        else:
            return(False, True)
    except:
        return(False, False)
