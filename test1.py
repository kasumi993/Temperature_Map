# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 20:32:16 2021

@author: vitor
"""

import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd
import sqlite3

# ouverture d'une connexion avec la base de données
conn = sqlite3.connect('Temperature_DB.db')
c = conn.cursor()


#pour recuperer station + temperature maximale
req = ("SELECT Numéro, Temp_maximales FROM 'Historiques_Temp'")
c.execute(req)
r = c.fetchall()
L = len(r)
    

#pour recuperer liste des station
#req = ("SELECT * FROM 'stations-meteo'")
#c.execute(req)
#liste_stations = c.fetchall()
#data = []

#for station in liste_stations:
#    donnee = {}
#    donnee['num']=station[0]
#    donnee['ville']=station[1]
#    donnee['lat']=station[2]
#    donnee['lon']=station[3]
#    donnee['alt']=station[4]
#    data.append(donnee)
    
    

def position_stations():
    """donne la longitude, la latitude et altitude des stations """
    conn = sqlite3.connect('Temperature_DB.db')
    curseur = conn.cursor()
    curseur.execute("SELECT Numero, Ville, Longitude, Latitude FROM 'stations-meteo'")
    liste_stations = c.fetchall()
    a=[]
    for station in liste_stations:
        donnee = {}
        donnee['num']=station[0]
        donnee['ville']=station[1]
        donnee['lat']=station[2]
        donnee['lon']=station[3]
        a.append(donnee)
    return a



def get_temp(nom_stat,tmoy,tmin,tmax,debut,fin):
    try:
        fin=int(fin[:4]+fin[5:7]+fin[8:])
        debut=int(debut[:4]+debut[5:7]+debut[8:])
        conn = sqlite3.connect('Temperature_DB.db')
        curseur = conn.cursor()
        if tmoy:
            curseur.execute("SELECT Temp_moyennes, DATE FROM 'Historiques_Temp' AS C JOIN 'stations-meteo' AS S ON S.NUMERO=C.NUMÉRO WHERE S.VILLE = ? AND C.Temp_moyennes= ? AND C.DATE > ? AND C.DATE < ? ",(nom_stat,0,debut,fin))
            tmoy_i=curseur.fetchall()
        elif tmax:
            curseur.execute("SELECT Temp_maximales, DATE FROM 'Historiques_Temp' AS C JOIN 'stations-meteo' AS S ON S.NUMERO=C.NUMÉRO WHERE S.VILLE = ? AND C.Temp_maximales= ? AND C.DATE > ? AND C.DATE < ? ",(nom_stat,0,debut,fin))
            tmoy_i=curseur.fetchall()
        else:
            curseur.execute("SELECT Temp_minimales, DATE FROM 'Historiques_Temp' AS C JOIN 'stations-meteo' AS S ON S.NUMERO=C.NUMÉRO WHERE S.VILLE = ? AND C.Temp_minimales= ? AND C.DATE > ? AND C.DATE < ? ",(nom_stat,0,debut,fin))
            tmoy_i=curseur.fetchall()
        t=[]
        for x in tmoy_i:
            z=str(x[1])
            s=(z[:4],z[4:6],z[6:])
            t.append((x[0]/10,s))
        return t
               
    except Exception as err:                     # interception d'une exception quelconque
           print('Exception: ', type(err).__name__)
           print('err: ', str(err))
                
