import pandas as pd
import psycopg2 as psy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from getpass import getpass

def Graphes(user, userdb, pwd):
	co = None
	try:
		co=psy.connect(host='berlin',database=userdb,user=user,password=pwd)

		print('''\nLe prochain graphique va afficher :
Le nom et le nombre de vidéos des 15 chaines étant le plus apparu en tendances''')
		var=input("Voulez-vous afficher ce graphe (O/n) ? ")
		if(var=='O' or var=='o' or var=='1'):
			datafr=pd.read_sql('''SELECT c.nom AS chaine, count(*) AS NbVids
									FROM Video v
										INNER JOIN Chaine c ON c.idChaine = v.Chaine
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

		print('''\nLe prochain graphique va afficher :
Le nombre de nouvelles vidéos en tendances en fonction des jours de la semaine''')
		var=input("Voulez-vous afficher ce graphe (O/n) ? ")
		if(var=='O' or var=='o' or var=='1'):
			datafr=pd.read_sql('''SELECT to_char(v.dateSortie,'Day') AS Jour, count(*) AS Nb 
									FROM Video v
									GROUP BY Jour 
									ORDER BY Nb DESC;''', con=co)
			fig=datafr.plot(x='jour', y='nb', color='red', legend=False, kind='bar', figsize=[8,8])
			fig.grid(axis='y')
			fig.set_xlabel('Jour')
			fig.set_ylabel('Nombre de vidéos')
			fig.set_ylim(bottom=10000)
			plt.title('Le nombre de nouvelles vidéos en tendances en fonction des jours de la semaine')
			plt.yticks(np.linspace(10000, datafr.nb[0], int((datafr.nb[0]/1000)+1)))
			plt.show() # Affichage

		print('''\nLe prochain graphique va afficher :
Le nombre de vidéos en tendance en fonction des heures de la journée''')
		var=input("Voulez-vous afficher ce graphe (O/n) ? ")
		if(var=='O' or var=='o' or var=='1'):
			datafr=pd.read_sql('''SELECT to_char(v.dateSortie,'HH24') AS Heure, count(*) AS Nb
									FROM Video v
									GROUP BY Heure
									ORDER BY Heure;''', con=co)
			fig=datafr.plot(x='heure', y='nb', legend=False, kind='bar', figsize=[8,8],color='red')
			fig.grid(axis='y')
			fig.set_xlabel('Heure')
			fig.set_ylabel('Nombre de vidéos')
			fig.set_ylim(bottom=100)
			plt.title('Le nombre de vidéos en tendance en fonction des heures de la journée')
			plt.yticks(np.linspace(100, max(datafr.nb), int(max(datafr.nb)/1000)+1))
			plt.show() # Affichage




		print('''\nLe prochain graphique va afficher :
Pourcentage du nombre de videos par categories''')
		var=input("Voulez-vous afficher ce graphe (O/n) ? ")
		if(var=='O' or var=='o' or var=='1'):
			datafrpie=pd.read_sql('''SELECT ca.nom AS categorie, 
									round((count(*) / ((SELECT count(*) FROM Video)*1.0)*100),2) AS pourcent
									FROM Video v
									INNER JOIN Categorie ca ON ca.idCategorie = v.categorie
									WHERE ca.nom != 'NaN'
									GROUP BY ca.idCategorie;''', con=co)
			datafrpie.groupby(['categorie']).sum().plot(kind='pie', y='pourcent',autopct='%1.0f%%',
                                title='Pourcentage du nombre de videos par categories',legend=False,figsize=[8,8],)
			plt.axis('off')
			plt.show()

		print('''\nLe prochain graphique va afficher :
Pourcentage de likes et dislikes par rapport aux vues pour chaque catégorie''')
		var=input("Voulez-vous afficher ce graphe (O/n) ? ")
		if(var=='O' or var=='o' or var=='1'):
			datafr=pd.read_sql('''SELECT ca.nom AS Categorie, round((sum(v.likes)/sum(v.vues)*1.0)*100,2) AS LIKES, 
								round((sum(v.dislikes)/sum(v.vues)*1.0)*100,2) AS DISLIKES
								FROM Video v
								INNER JOIN categorie ca ON ca.idcategorie = v.categorie
								WHERE ca.nom != 'NaN'
								GROUP BY ca.idcategorie;''', con=co)
			

			fig = datafr.plot.barh(x='categorie',stacked=True,figsize=[8,8],title='Pourcentage de likes et dislikes par rapport aux vues pour chaque catégorie')
			fig.set_xlabel('Pourcentage d\'avis')
			fig.set_ylabel('Categories')
			plt.show()

		print('''\nLe prochain graphique va afficher :
Temps qui s'écoule entre la publication et le passage tendance d'une video''')
		var=input("Voulez-vous afficher ce graphe (O/n) ? ")
		if(var=='O' or var=='o' or var=='1'):
			datafr=pd.read_sql('''SELECT count(*) AS Video,to_char((dateTendance-dateSortie) ,'DD') AS NbJours
									FROM Video
									GROUP BY NbJours
									ORDER BY NbJours;''', con=co)
			

			fig = datafr.plot.bar(x='nbjours',y='video',stacked=True,figsize=[8,8],title='Temps qui s’écoule entre la publication et le passage tendance d\'une video')
			fig.set_xlabel('Jours')
			fig.set_ylabel('Nombre de vidéos')
			plt.show()

		print('''\nLe prochain graphique va afficher :
Nombre de vidéos qui passent en tendance par année''')
		var=input("Voulez-vous afficher ce graphe (O/n) ? ")
		if(var=='O' or var=='o' or var=='1'):
			datafr=pd.read_sql('''SELECT count(*) AS nbvids , to_char(dateSortie,'YYYY') AS annee
								FROM Video
								GROUP BY annee
								ORDER BY annee;''', con=co)
			

			fig = datafr.plot.bar(x='annee',y='nbvids',stacked=True,figsize=[8,8],title='Nombre de vidéos qui passent en tendance par année')
			fig.set_xlabel('Année')
			fig.set_ylabel('Nombre de vidéos')
			plt.show()


	except(Exception,psy.DatabaseError) as error:
		print(error)
	finally:
		if co is not None:
			co.close()

user=input("Nom d'utilisateur : ")
pwd = getpass(prompt="Mot de passe : ")
userdb = "db" + user 
Graphes(user, userdb, pwd)
