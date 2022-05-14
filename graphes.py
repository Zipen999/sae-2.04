import pandas as pd
import psycopg2 as psy
import numpy as np
import matplotlib.pyplot as plt

from getpass import getpass

def Graphes(user, userdb, pwd):
	co = None
	try:
		co=psy.connect(host='berlin',database=userdb,user=user,password=pwd)

		print('''\nLe prochain graphique va afficher :
Le nom et le nombre de vidéos des 15 chaines étant le plus apparu en tendances''')
		var=input("Voulez-vous afficher ce graphe (O/n) ? ")
		if(var=='O' or var=='o' or var==1):
			datafr=pd.read_sql('''SELECT c.nom AS chaine, count(*) AS NbVids
									FROM Video v
										INNER JOIN Publier p ON v.idVideo = p.Video
										AND v.dateTendance = p.dateTendance
										INNER JOIN Chaine c ON c.idChaine = p.Chaine
											GROUP BY c.nom
											ORDER BY NbVids DESC
											LIMIT 15;''', con=co)
			fig=datafr.plot(x='chaine', y='nbvids', color='red', legend=False, kind='bar', figsize=[8,8])
			fig.grid(axis='y')
			fig.set_xlabel('Chaine')
			fig.set_ylabel('Nombre de vidéos')
			plt.title('Les chaines ayant eu le plus de vidéos en tendances')
			plt.yticks(np.linspace(0, datafr.nbvids[0], int((datafr.nbvids[0]/100)+1)))
			plt.show() # Affichage

	except(Exception,psy.DatabaseError) as error:
		print(error)
	finally:
		if co is not None:
			co.close()

user=input("Nom d'utilisateur : ")
pwd = getpass(prompt="Mot de passe : ")
userdb = "db" + user 
Graphes(user, userdb, pwd)