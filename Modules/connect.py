#!/usr/bin/env python3.9
import mysql.connector

#--------------BDD A COPIER----------------
def Copy_Connect():
    #Paramètres BDD à copier
    Copy = mysql.connector.connect(
        host="127.0.0.1",
        port ="3306",
        database ="test",
        user="leo",
        password="leoadsbnetwork"
    )
    return Copy
#--------------BDD A COLLER----------------
def Paste_Connect():
    #Paramètres BDD sur laquelle coller
    Paste = mysql.connector.connect(
        host="127.0.0.1",
        port ="6603",
        database ="completeBDD",
        user="leo",
        password="leoadsbnetwork"
    )
    return Paste