#-*- coding: utf-8 -*-

import mysql.connector

def getPatients():
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            database = "soigne_moi",
            user = "root",
            password = ""
        )
        mycursor = mydb.cursor()
        sql = """SELECT * FROM user WHERE roles LIKE '%ROLE_USER%' ORDER BY lastname"""
        mycursor.execute(sql)
        patients = mycursor.fetchall()
        mydb.close()
        return(patients)
    except:
        print("Oups")