#!/usr/bin/env python3.9
import datetime, re
from mysql.connector import Error
from Modules.functions import Aircrafts, Airports, Socair, Unicode, File
from Modules.connect import Copy_Connect, Paste_Connect
from Modules.spatial import Spatial

startTime = datetime.datetime.now()
#--------------------------BDD--------------------------
copy = Copy_Connect()
paste = Paste_Connect()
#Réinitialise le fichier avec les erreurs d'insertions
txt = open('Txt/errorinsertion.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
txt = open('Txt/?.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
txt = open('Txt/errortable.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
txt = open('Txt/errorselect.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
try:
    #Connexion BDD à copier
    if copy.is_connected():
        copy_info = copy.get_server_info()
        copy_cursor = copy.cursor()
        copy_cursor.execute("Select Database();")
        rowloc = copy_cursor.fetchone()
    #Connexion BDD sur laquelle coller
    if paste.is_connected():
        paste_info = paste.get_server_info()
        paste_cursor = paste.cursor()
        paste_cursor.execute("Select Database();")
        rowloc = paste_cursor.fetchone()
except Error as e:
    print("Erreur de connexion à MySQL", e)

#--------------------------CREATION TABLE ET INSERTION DONNEES--------------------------
#Fichier txt avec le nom des tables à copier
listetable = open('Txt/liste', encoding='utf-8', mode='r')
for table in listetable:
    #Utiliser pour insérer les données
    newtable = str(table).replace("('","").replace("',)","").replace("rvcontrib.","").replace("radarvirtuel.","").replace("meteo.","").strip().lower()
    #Obtiens les informations sur la table
    desc_table = "DESC %s" % (table)
    copy_cursor.execute(desc_table)
    colonne_data = copy_cursor.fetchall()
    #Obtiens les index de la table
    index_table = "SHOW INDEX FROM %s" % (table)
    copy_cursor.execute(index_table)
    index_data = copy_cursor.fetchall()
    #Compte le nb de tuples dans la table
    count_query = "SELECT COUNT(*) FROM %s" % (table)
    copy_cursor.execute(count_query)
    count_rows = copy_cursor.fetchone()
    #Variable du nb de tuples
    numberofrows = count_rows[0]
    #--------------------------CREATION DES TABLES--------------------------
    #String de chaque colonne de la table
    colonnequery = ""
    #String des index de la table
    indexquery=""
    #String du nom du champ de la table
    cptfield=""
    #Compte le nombre de champs
    cptrow= -1
    #Permet de savoir le type de données qu'on insère
    strtype =""
    #Permet de savoir si la valeur de la donnée est nulle ou non
    strnull =""
    #Permet de savoir si c'est une clé primaire
    strkey =""
    #Liste des champs de la clé primaire
    fieldkey =""
    #Liste de tous les champs de la table
    strfield =""
    #Liste de tous les index de la table
    strindex=""
    #Liste des champs composant l'index
    strfieldindex=""
    #Liste des index / clé
    keyname=""
    #Chaque index de la table
    for index in index_data:
        keyname = index[2]
        colonne = index[4]
        null = index[9]
        indextype = index[10]
        strfieldindex = strfieldindex+colonne+","
        strindex = strindex + keyname+","
    manyindex = strindex.count(keyname)
    #Chaque colonne de la table
    for colonne in colonne_data:
        spatial = False
        field = colonne[0]
        #Nom de colonne en minuscule
        field = str(field).lower()
        cptfield = cptfield + field+","
        type = colonne[1]
        null = colonne[2]
        key = colonne[3]
        default = colonne[4]
        extra = colonne[5]

        #String de tous les types de la table
        strtype = strtype + type+","
        #String de tous les null de la table
        strnull = strnull + null+","
        #String de toutes les key de la table
        strkey = strkey + key+","

        #Test si le type est SPATIAL
        if any(word == type for word in("point","multipoint","polygon","multipolygon","geometry","geometrycollection","linestring","multilinestring")):
            spatial = True
        #String de tous les champs de la table
        if spatial==True:
            strfield = strfield + "ST_AsText("+field+"),"
        else:
            strfield = strfield + field+","

        if spatial==True and key!="":
            indexquery = indexquery+"SPATIAL INDEX (%s)," %(field)
        if null == "NO":
            null = "NOT NULL"
        else:
            null = ""
        if key == "PRI" and spatial == False:
            key = "PRIMARY KEY"
            fieldkey = fieldkey +field+","
        elif key == "MUL":
            key =""
            if spatial == False:
                indexquery = indexquery+"INDEX (%s)," % (field)
        elif key == "UNI":
            key = "UNIQUE"
        if default == None or default =="":
            default = ""
        elif isinstance(default, int) or default =="current_timestamp()":
            default = "Default %s"% (default)
        elif isinstance(default, str) and default !="current_timestamp()":
            default = "Default '%s'" % (default)

        colonnequery = colonnequery+field+" "+type+" "+null+" "+key+" "+default+" "+extra+","
        cptrow +=1
        
    #String des champs de la table à utiliser dans le select
    size = len(strfield)
    newstrfield = strfield[:size -1]
    #Test si plusieurs champs dans la clé primaire
    manypri = colonnequery.count("PRI")
    #Si clé primaire composé
    if manypri ==0 and manyindex ==0:
        create_table = "CREATE TABLE IF NOT EXISTS %s(%s) ENGINE = MYISAM" % (newtable,colonnequery)
        print(newcreatetable)
        paste_cursor.execute(newcreatetable)
    if manypri ==0 and manyindex!=1:
        indexquery = "INDEX %s (%s)" % (keyname,strfieldindex)
    if manypri != 0 and manyindex!=1:
        #Liste des champs composant la clé primaire
        listfieldkey = fieldkey.split(',')
        #Nom de la clé primaire = nom du premier champ
        namepri = listfieldkey[0]
        colonnequery = colonnequery.replace("PRIMARY KEY","")
        indexquery = indexquery+"CONSTRAINT %s PRIMARY KEY(%s)" % (namepri,fieldkey)
    #Liste des types
    listtype = strtype.split(',')
    #Liste des null
    listnull = strnull.split(',')
    #Liste des clés
    listkey = strkey.split(',')
    #Liste des champs
    listfield = strfield.split(',')
    #String de chaque colonne de la table
    colonnequery = colonnequery+indexquery
    #Requete SQL pour créer la table
    create_table = "CREATE TABLE IF NOT EXISTS %s(%s) ENGINE = MYISAM" % (newtable,colonnequery)
    newcreatetable = create_table.replace(",)",")").replace("'CURRENT_TIMESTAMP()'","CURRENT_TIMESTAMP()").replace("'CURRENT_TIMESTAMP'","CURRENT_TIMESTAMP")
    print(newcreatetable)
    try:
        paste_cursor.execute(newcreatetable)
    except:
        txt = open('Txt/errortable.txt',encoding='utf-8',mode='a')
        txt.write(newcreatetable+"\n")
        txt.close()

    #--------------------------INSERTION DES DONNEES--------------------------
    cptselect = 0
    limit = 0
    #Si nb de tuples = 0, passe à la table suivante
    if numberofrows == 0:
        cptselect = numberofrows +1
    while cptselect < numberofrows:
        #Nombre de lignes à insérer
        diff = numberofrows - cptselect
        #Permet de savoir combien de tuples à sélectionner à la fois
        divpar = str(diff)[0] + str((len(str(diff))-1)*"0")
        limit = int(divpar)
        if diff > 100000:
            limit //= 2
        print("Données de la table :",newtable,"Nombre de lignes restantes à insérer :",diff,"Nombre de lignes insérées à la fois : ",limit)
        #Requete SQL pour sélectionner les tuples
        select_table = "SELECT %s FROM %s LIMIT %s,%s;" % (newstrfield,table,cptselect,limit)
        try:
            copy_cursor.execute(select_table)
        except:
            txt = open('Txt/errorselect.txt',encoding='utf-8',mode='a')
            txt.write(select_table+"\n")
            txt.close()
        select_data = copy_cursor.fetchall()
        #Dictionnaire avec les valeurs à insérer
        typedic=""
        timetoinsert = datetime.datetime.now()
        for row in select_data:
            dictionaryvalues = ""
            cpt = 0
            while cpt <= cptrow:
                #Donne le type de chaque données qu'il faut inséré
                newtype = str(listtype[cpt])
                #Enlève les numéros et les parenthèses
                newtype = re.sub("\d+", "", newtype).replace("()","")
                spatialdic = False
                #Dit si une donnée peut etre nulle ou non
                newnull = str(listnull[cpt])
                #Dit si une clé est primaire
                newkey = str(listkey[cpt])
                #Donne le nom du champ
                newfield = str(listfield[cpt])
                #Prend les données une à une et enlève les espaces de début et de fin, enlève les accents
                newrow = Unicode(str(row[cpt]), newkey)
                #--------------------------TRI DES TYPES--------------------------
                if (newnull =="YES" and newrow=="None") or (newnull=="YES" and newrow=="NONE"):
                    newrow ="NULL"
                if (newtype=="timestamp" and newnull=="NO" and newrow=="None") or (newtype=="datetime" and newrow=="None"):
                    newrow ="0000:00:00 00-00-00"

                #Tri spécifique pour ces tables
                if newtable =="aircrafts":
                    newrow = Aircrafts(newrow,newfield)
                    #Changement du countryicao par les données dans la table country
                    if newfield=="countryicao" and len(newrow) >2:
                        try:
                            query = f"SELECT countrycode FROM `country` WHERE countryname ='{newrow}'"
                            copy_cursor.execute(query)
                            #Récupère le countrycode
                            countrycode = str(copy_cursor.fetchone()[0]).title()
                            if countrycode:
                                newrow = countrycode
                            newrow = newrow
                        except:
                            newrow = newrow
                elif newtable =="socair":
                    newrow = Socair(newrow,newfield)
                elif newtable =="airports":
                    newrow = Airports(newrow,newfield, newkey)

                #Gestion des types spatials
                if newtype=="multipolygon" or newtype =="polygon" or newtype=="point":
                    spatialdic = True
                    typedic = typedic + newtype+","
                    newrow = Spatial(newrow, newtype)
                    dictionaryvalues = dictionaryvalues + newrow

                if spatialdic == False:
                    dictionaryvalues = dictionaryvalues + '"'+newrow.replace('"'," ")+'",'
                cpt +=1
            #Supprime le dernier caractère de la chaine (la virgule)
            size = len(dictionaryvalues)
            newdictionaryvalues = dictionaryvalues[:size -1]
            #REGEX et replace
            newdictionaryvalues = newdictionaryvalues.replace('"NULL"','NULL').replace("'"," ")
            insert_data = "REPLACE INTO %s VALUES (%s)" % (newtable,newdictionaryvalues)
            if ("?" in insert_data and "http" not in insert_data and "php" not in insert_data) or ("�" in insert_data):
                File(insert_data)
                continue
            #Gestion des erreurs d'insertion dans la BDD
            try:
                paste_cursor.execute(insert_data)
            except Error as e:
                print("Erreur dans l'insertion", e)
                txt = open('Txt/errorinsertion.txt',encoding='utf-8',mode='a')
                txt.write(insert_data+"\n")
                txt.close()
            #compteur en fonction du nb de tuples dans la table
        cptselect = cptselect + limit
        print("Temps d'insertion pour",limit,"tuples :",datetime.datetime.now()-timetoinsert)

#Permet d'insérer la dernière table
create_table = "CREATE TABLE ASUPPRIMER( asupprimer varchar (20))"
paste_cursor.execute(create_table)
drop_table = "DROP TABLE ASUPPRIMER"
paste_cursor.execute(drop_table)

if copy.is_connected() and paste.is_connected():
    copy_cursor.close()
    copy.close()
    paste_cursor.close()
    paste.close()
    print("Connexion à la BDD locale fermée")
    print("Connexion à la BDD copy fermée")
print(datetime.datetime.now()-startTime)