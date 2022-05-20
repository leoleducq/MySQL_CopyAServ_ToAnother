#!/usr/bin/env python3.9
import unidecode
def Unicode(newrow, newkey):
    #Enleve les accents et les espaces
    newrow = unidecode.unidecode(newrow).strip()
    #Ne pas enlever le ?, Mettre la chaine en minuscule
    if any(word in newrow for word in("http","php","@")):
        newrow=newrow.lower()
    elif newkey!="":
        newrow = newrow.upper()
    return newrow

#Table AIRCRAFTS    
def Aircrafts(newrow, newfield):
#------------STRING-----------------------
    newrow = str(newrow)

#-------Enlever / Remplacer les ?---------
    
    #Supprime le ?
    if newfield=="serialnu" or newfield=="model":
        newrow = newrow.replace("?","")
    #Remplace toute la chaine par une chaine vide
    if (newfield =="registeredowener") or (newfield=="icaoportattache" and len(newrow)<=4):
        newrow=""
    #Remplace le ? par un -
    elif newfield =="regcode":
        newrow = newrow.replace("?","-")
    #Pour les A
    newrow = newrow.replace("H?NLE","HANLE")
    #Pour les U
    newrow = newrow.replace("B?CKER","BUCKER").replace("na?tica","nautica").replace("LUFTAUSR?STUNG","LUFTAUSRUSTUNG")
    newrow = newrow.replace("GLASFL?GEL","GLASFLUGEL")
    #Pour les E
    newrow = newrow.replace("A?RO","AERO").replace("A?ro","Aero").replace("SOCI?T?","SOCIETE")
    newrow = newrow.replace("Z?RO","ZERO").replace("Gu?pard","Guepard").replace("FI?RES","FIERES")
    newrow = newrow.replace("SPORTIN?","SPORTINE").replace("Ja?n","Jaen")
    #Pour les O
    newrow = newrow.replace("W?RNER","WORNER").replace("BAL?NY","BALONY").replace("B?LKOW","BOLKOW")
    #Pour les I
    newrow = newrow.replace("KUB?CEK","KUBICEK")

#---------Formatage----------
    
    #Met la chaine en majuscule
    if any(word == newfield for word in("icaotypecode","typemodel","serialnu","icaoowener","iconname","operateurcodeflag","majuser")):
        newrow = newrow.upper()
    #Met la 1ere lettre en majuscule
    if (any(word == newfield for word in("type","countryicao","categorie","registeredowener","typemoteur","manufacturer"))) and (newrow!="NULL") and (all(word not in newrow for word in("http","php","@"))):
        newrow = newrow.title()

#-----------FIN---------------
    return newrow

#Table SOCAIR
def Socair(newrow, newfield):
    newrow = str(newrow)
    newrow = newrow.replace("Aviac?o","Aviacao")

    #Met la chaine en majuscule
    if any(word == newfield for word in("codepays","iconname","callsign")):
        newrow = newrow.upper()
    if any(word == newfield for word in ("designation","pays","activite")):
        newrow = newrow.title()
    
    return newrow
#Table AIRPORTS
def Airports(newrow,newfield, newkey):
    newrow = str(newrow)
    newrow = newrow.replace("?","")
    
    #Met la chaine en majuscule
    if newfield=="continent":
        newrow = newrow.upper()
    elif newfield=="pays":
        newrow = newrow[:2].upper()
    #Met la 1ere lettre en majuscule
    elif newfield!="infourl" and newkey=="":
        newrow=newrow.title()
    return newrow
    
#Ecrit dans un fichier
def File(texte):
    txt = open('Txt/?.txt',encoding='utf-8',mode='a')
    txt.write(texte+"\n")
    txt.close()