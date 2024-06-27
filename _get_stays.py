#-*- coding: utf-8 -*-

import mysql.connector

def getStays():
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            database = "soigne_moi",
            user = "root",
            password = ""
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM stay")
        stays = mycursor.fetchall()
        mydb.close()
        return(stays)
    except:
        return(False)

def getStayUser(id):
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            database = "soigne_moi",
            user = "root",
            password = ""
        )
        mycursor = mydb.cursor()
        sql = """SELECT * FROM user WHERE id = ("%s")""" %(id)
        mycursor.execute(sql)
        user = mycursor.fetchone()
        mydb.close()
        return(user)
    except:
        return(False)

def getStaySpecialty(id):
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            database = "soigne_moi",
            user = "root",
            password = ""
        )
        mycursor = mydb.cursor()
        sql = """SELECT * FROM specialty WHERE id = ("%s")""" %(id)
        mycursor.execute(sql)
        specialty = mycursor.fetchone()
        mydb.close()
        return(specialty)
    except:
        return(False)