import sqlite3
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.axis

mois = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']


#connexion à la base de donnée
try :
    conn=sqlite3.connect('TemperatureDB.db')
    c=conn.cursor()
    print("connexion à la base de donnée réussie")
except Exception as err:
    print("erreur de connexion à la base de donnee",err)


#on formate l'affichage de la logitude pour passer de l'ecriture dms à décimal




# définition du handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):
  global conn
  global c
    
# sous-répertoire racine des documents statiques
  static_dir = '/client'

# cette fonction sert à modifier directement le format des latitudes/longitudes
# # decommenter pour utiliser
#    def conversion(chaine):
#      signe = chaine[0]
#      chaine = chaine.split(':')
#      degre = abs(float(chaine[0]))
#      minute = float(chaine[1])
#      seconde = float(chaine[2])
#      DD = degre + minute/60 + seconde/3600
#      if signe == '+':
#          return DD
#      else:
#          return -DD
    
    
#    c.execute("SELECT Numero,Latitude,Longitude FROM 'stations-meteo'")
#    resultat=c.fetchall()
#    print(resultat[1])

#    for i in range(len(resultat)):
#      c.execute("UPDATE 'stations-meteo' SET Latitude=?, Longitude= ? WHERE Numero = ?",(conversion(resultat[i][1]),conversion(resultat[i][2]),resultat[i][0]))
#      conn.commit()

#fin fonction modification base de donnée

  # on surcharge la méthode qui traite les requêtes GET
  def do_GET(self):
    global c
    self.init_params()
    print("path info: "+str(self.path_info))

    # requete location - retourne la liste de lieux et leurs coordonnées géographiques
    if self.path_info[0]=='location_station':
        data=[]
        c.execute("SELECT * FROM 'stations-meteo'")
        liste_stations = c.fetchall()
        for station in liste_stations:
            donnee  = {}
            donnee['num']=station[0]
            donnee['ville']=station[1]
            donnee['lat']=station[2]
            donnee['lon']=station[3]
            donnee['alt']=station[4]
            data.append(donnee)
        self.send_json(data)
        
        
    # requête générique
    elif self.path_info[0] == "service":
      self.send_html('<p>Path info : <code>{}</p><p>Chaîne de requête : <code>{}</code></p>' \
          .format('/'.join(self.path_info),self.query_string));

    else:
      self.send_static()


  # méthode pour traiter les requêtes HEAD
  def do_HEAD(self):
      self.send_static()


  # méthode pour traiter les requêtes POST - non utilisée dans l'exemple
  def do_POST(self):
    self.init_params()
    data=[]
    donnee={}
    
    # requête générique
    if self.path_info[0] == "recherches":
      print("voila")
      print(self.params["datepicker_start"])
      #Renommage des variables envoyées par le formulaire
      self.start_date=str(self.params["datepicker_start"][0]).split("-")
      self.end_date=str(self.params["datepicker_end"][0]).split("-")
      
                     
      self.jour_debut = self.start_date[2]
      self.jour_fin = self.end_date[2]
      self.mois_debut = self.start_date[1]
      self.mois_fin = self.end_date[1]
      self.annee_debut = self.start_date[0]
      self.annee_fin =self.end_date[0]
      self.zone = self.params['zone'][0]   
      
                    
      if self.zone == 'france':
          nom_courbe_moy = courbe_nationale([0,0,1],self.jour_debut,self.mois_debut,self.annee_debut,self.jour_fin,self.mois_fin,self.annee_fin)
          nom_courbe_min = courbe_nationale([1,0,0],self.jour_debut,self.mois_debut,self.annee_debut,self.jour_fin,self.mois_fin,self.annee_fin)
          nom_courbe_max = courbe_nationale([0,1,0],self.jour_debut,self.mois_debut,self.annee_debut,self.jour_fin,self.mois_fin,self.annee_fin)
          donnee['nom_courbe_moy']=nom_courbe_moy
          donnee['nom_courbe_min']=nom_courbe_min
          donnee['nom_courbe_max']=nom_courbe_max
          data.append(donnee)
          self.send_json(data)

      else:
          self.id_station = int(self.params['id_station'][0])
          nom_courbe_moy = self.courbe_station([0,0,1],self.id_station,self.jour_debut,self.mois_debut,self.annee_debut,self.jour_fin,self.mois_fin,self.annee_fin)
          nom_courbe_min = self.courbe_station([1,0,0],self.id_station,self.jour_debut,self.mois_debut,self.annee_debut,self.jour_fin,self.mois_fin,self.annee_fin)
          nom_courbe_max = self.courbe_station([0,1,0],self.id_station,self.jour_debut,self.mois_debut,self.annee_debut,self.jour_fin,self.mois_fin,self.annee_fin)
          donnee['nom_courbe_moy']=nom_courbe_moy
          donnee['nom_courbe_min']=nom_courbe_min
          donnee['nom_courbe_max']=nom_courbe_max
          data.append(donnee)
          self.send_json(data)
    else:
      self.send_error(405)


  # on envoie le document statique demandé
  def send_static(self):

    # on modifie le chemin d'accès en insérant le répertoire préfixe
    self.path = self.static_dir + self.path

    # on calcule le nom de la méthode parent à appeler (do_GET ou do_HEAD)
    # à partir du verbe HTTP (GET ou HEAD)
    method = 'do_{}'.format(self.command)

    # on traite la requête via la classe parent
    getattr(http.server.SimpleHTTPRequestHandler,method)(self)


  # on envoie un document html dynamique
  def send_html(self,content):
     headers = [('Content-Type','text/html;charset=utf-8')]
     html = '<DOCTYPE html><html><title>{}</title><link rel="stylesheet" type="text/css" href="style.css"/><meta charset="utf-8">{}</html>' \
         .format(self.path_info[0],content)
     self.send(html,headers)

  # on envoie un contenu encodé en json
  def send_json(self,data,headers=[]):
    body = bytes(json.dumps(data),'utf-8') # encodage en json et UTF-8
    self.send_response(200)
    self.send_header('Content-Type','application/json')
    self.send_header('Content-Length',int(len(body)))
    [self.send_header(*t) for t in headers]
    self.end_headers()
    self.wfile.write(body) 

  # on envoie la réponse
  def send(self,body,headers=[]):
     encoded = bytes(body, 'UTF-8')

     self.send_response(200)

     [self.send_header(*t) for t in headers]
     self.send_header('Content-Length',int(len(encoded)))
     self.end_headers()

     self.wfile.write(encoded)


  # on analyse la requête pour initialiser nos paramètres
  def init_params(self):
    # analyse de l'adresse
    info = urlparse(self.path)
    self.path_info = info.path.split('/')[1:]
    self.query_string = info.query
    self.params = parse_qs(info.query)

    # récupération du corps
    length = self.headers.get('Content-Length')
    ctype = self.headers.get('Content-Type')
    if length:
      self.body = str(self.rfile.read(int(length)),'utf-8')
      if ctype == 'application/x-www-form-urlencoded' : 
        self.params = parse_qs(self.body)
    else:
      self.body = ''

    print(length,ctype,self.body, self.params)
    
#==============================================================================
# Format : fonction qui change la forme de la date.
#En entre une date du type '20120201'
#☻En sortie on a '01/02/2012'
#==============================================================================
  def format(S):
    return(S[-2]+S[-1]+'/'+S[-4]+S[-3]+'/'+S[0]+S[1]+S[2]+S[3])    


    
  def courbe_station(self,courbes,id_station,jour_1,mois_1,annee_1,jour_2,mois_2,annee_2):
        """fonction pour afficher les courbes par station"""
        
        id_station = int(id_station)
        c.execute("SELECT Ville from 'stations-meteo' WHERE Numero = {}".format(id_station))
        nom_station = str(c.fetchall()).strip('[').strip(']').strip('(').strip(')').strip(',').strip("'")

        
        date1, date2 = '',''
        date1 = int(annee_1+mois_1+jour_1)
        date2 = int(annee_2+mois_2+jour_2)

        c.execute('SELECT Temp_moyennes, Temp_minimales, Temp_maximales, Q_TG, Q_TN, Q_TX, DATE from Historique_Temp WHERE Numero = {} AND date >= {} AND date < {} ORDER BY date ASC'.format(id_station, date1, date2))
        data = c.fetchall()
        
        Tmoy, Tmin, Tmax = [],[],[]
        time=[]
        TimeDate=[]
        i=0
        
        for releves in data:
            if releves[3]==0 and releves[4]==0 and releves[5]==0:
                Tmoy.append(0.1*releves[0])
                Tmin.append(0.1*releves[1])
                Tmax.append(0.1*releves[2])
                TimeDate.append(str(releves[6]))
                time.append(i)
            i+=1  
        
            
            
        plt.figure(figsize=(10,6), dpi=100)        
        plt.grid(True)
        plt.xlabel('Dates')
        plt.ylabel('T en °C')
        plt.title('        Relevé de températures sur la période ['+jour_1+'/'+mois_1+'/'+ \
        annee_1+'-'+jour_2+'/'+mois_2+'/'+annee_2+'] à '+str(nom_station),fontsize=10)

        n=len(time)    
        
        if courbes[0]==1:
            
            plt.plot(time, Tmin, label='Températures minimales',color='b')
            plt.xticks([0,n//4,n//2,3*n//4,n-1],[format(TimeDate[0]),format(TimeDate[n//4]),format(TimeDate[n//2]),format(TimeDate[3*n//4]),format(TimeDate[-1])])
        
        if courbes[1]==1:
            plt.plot(time, Tmax, label='Températures maximales',color='r')
            plt.xticks([0,n//4,n//2,3*n//4,n-1],[format(TimeDate[0]),format(TimeDate[n//4]),format(TimeDate[n//2]),format(TimeDate[3*n//4]),format(TimeDate[-1])])
            
        if courbes[2]==1:
            plt.plot(time, Tmoy, label='Températures moyennes',color='g')
            plt.xticks([0,n//4,n//2,3*n//4,n-1],[format(TimeDate[0]),format(TimeDate[n//4]),format(TimeDate[n//2]),format(TimeDate[3*n//4]),format(TimeDate[-1])])
        
        plt.legend(fontsize=10,loc=4)
        plt.savefig('client/Plot/'+str(id_station)+'_'+str(date1)+str(date2)+str(courbes[0])+str(courbes[1])+str(courbes[2])+'.png',bbox_inches='tight')
        titre=str(id_station)+'_'+str(date1)+str(date2)+str(courbes[0])+str(courbes[1])+str(courbes[2])+'.png'
        
        #Remplissage de la table courbe_stations
        c.execute('INSERT INTO courbes_stations VALUES (?,?,?,?,?,?,?)',(titre,id_station,date1,date2,courbes[0],courbes[1],courbes[2]))
        conn.commit()          
        return(str(id_station)+'_'+str(date1)+str(date2)+str(courbes[0])+str(courbes[1])+str(courbes[2])+'.png')
        
        
 
def courbe_nationale(courbes,jour_1,mois_1,annee_1,jour_2,mois_2,annee_2):
    """fonction pour afficher les courbes en faisant la moyenne nationale"""
    
    date1, date2 = '',''
    date1 = int(annee_1+mois_1+jour_1)
    date2 = int(annee_2+mois_2+jour_2)
    
    id_stations=[33,34,37,737,738,742,745,749,750,757,758,434,39,322,2207,11246,11249] #liste des station avec des données
    #station sans données : 31,32,36,736,739,740,755,756,786,793,323,784,2184,2190,2192,2195,2196,2199,2200,2203,2205,2209,11243,11244,11245,11247,11248
    conn=sqlite3.connect('TemperatureDB.db')
    c=conn.cursor() 

    TimeDate=[] #liste des dates
    sta='33'
    c.execute('SELECT DATE from Historique_Temp WHERE Numero = {} AND date >= {} AND date < {} ORDER BY date ASC'.format(sta, date1, date2))
    data = c.fetchall()
    for k in data:
        TimeDate.append(str(k[0]))
   
    Tmoy, Tmin, Tmax = [],[],[]  #listes des températures de chaque station
    Qmoy, Qmin, Qmax = [],[],[] #liste des qualitées des mesures
    for i in range(len(id_stations)):  
        station=id_stations[i]
        c.execute('SELECT Temp_moyennes, Temp_minimales, Temp_maximales, Q_TG, Q_TN, Q_TX from Historique_Temp WHERE Numero = {} AND date >= {} AND date < {} ORDER BY date ASC'.format(station, date1, date2))
        data = c.fetchall()
        Tmoy.append([])
        Tmin.append([])
        Tmax.append([])
        Qmoy.append([])
        Qmin.append([])
        Qmax.append([])    
        for releves in data:
            Tmoy[i].append(0.1*releves[0])
            Tmin[i].append(0.1*releves[1])
            Tmax[i].append(0.1*releves[2])
            Qmoy[i].append(releves[3])
            Qmin[i].append(releves[4])
            Qmax[i].append(releves[5])
    time = range(len(data))
    
    TempMoy,TempMin,TempMax=[],[],[]  #listes des températures à l'échelle nationale (moyenne des températures des stations)
    for i in range(len(Tmoy[0])):
        a,b,c=0,0,0
        Nmoy=len(Tmoy)
        Nmin=len(Tmin)
        Nmax=len(Tmax)
        N=Nmoy
        for j in range(N):
            if Qmoy[j][i]==0:        
                a+=Tmoy[j][i]
            else:
                Nmoy+=-1 #si la mesure est éronnée ou fausse, on ne la prend pas en compte dans la moyenne
            if Qmin[j][i]==0:
                b+=Tmin[j][i]
            else:
                Nmin+=-1
            if Qmax[j][i]==0:
                c+=Tmax[j][i]
            else:
                Nmax+=-1
        TempMoy.append(a/Nmoy)
        TempMin.append(b/Nmin)
        TempMax.append(c/Nmax)
    

    n=len(time)  
      
    plt.figure(figsize=(10,6), dpi=100)        
    plt.grid(True)
    plt.xlabel('Dates')
    plt.ylabel('T en °C')
    plt.title('        Relevé de températures sur la période ['+jour_1+'/'+mois_1+'/'+ \
    annee_1+'-'+jour_2+'/'+mois_2+'/'+annee_2+'] au niveau national ',fontsize=10)
    
    if courbes[0]==1:
        
        plt.plot(time, TempMin, label='Températures minimales',color='b')
        plt.xticks([0,n//4,n//2,3*n//4,n-1],[format(TimeDate[0]),format(TimeDate[n//4]),format(TimeDate[n//2]),format(TimeDate[3*n//4]),format(TimeDate[-1])])
    
    if courbes[1]==1:
        plt.plot(time, TempMax, label='Températures maximales',color='r')
        plt.xticks([0,n//4,n//2,3*n//4,n-1],[format(TimeDate[0]),format(TimeDate[n//4]),format(TimeDate[n//2]),format(TimeDate[3*n//4]),format(TimeDate[-1])])
        
    if courbes[2]==1:
        plt.plot(time, TempMoy, label='Températures moyennes',color='g')
        plt.xticks([0,n//4,n//2,3*n//4,n-1],[format(TimeDate[0]),format(TimeDate[n//4]),format(TimeDate[n//2]),format(TimeDate[3*n//4]),format(TimeDate[-1])])
    
    plt.legend(fontsize=10,loc=4)
    plt.savefig('client/Plot/'+'national'+'_'+str(date1)+str(date2)+str(courbes[0])+str(courbes[1])+str(courbes[2])+'.png',bbox_inches='tight')
    titre='national'+'_'+str(date1)+str(date2)+str(courbes[0])+str(courbes[1])+str(courbes[2])+'.png'
    #Remplissage de la table courbe_stations

    c.execute('INSERT INTO courbes_france VALUES (?,?,?,?,?,?)',(titre,date1,date2,courbes[0],courbes[1],courbes[2]))
    conn.commit()
    return('national'+'_'+str(date1)+str(date2)+str(courbes[0])+str(courbes[1])+str(courbes[2])+'.png')




# instanciation et lancement du serveur
httpd = socketserver.TCPServer(("", 80), RequestHandler)
httpd.serve_forever()
