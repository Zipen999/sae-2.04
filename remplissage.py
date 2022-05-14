import pandas as pd
import psycopg2 as psy
import json

from getpass import getpass

def Table(user, userdb, pwd):
	data=pd.read_csv(r'TrendingFR.csv')
	df=pd.DataFrame(data)
	df = df.drop_duplicates(subset=['video_id' , 'trending_date']) # Supprime les lignes dupliquées (Vidéos passés en tendances le même jour, impossible à traiter / incohérent sur youtube car une video peut passer en tendance une fois par jour)
	################### TRAITEMENT DES CATEGORIES
	id_vers_categorie = {}
	with open('FR_category_id.json', 'r') as f:
	    data = json.load(f)
	    for cat in data['items']:
	        id_vers_categorie[cat['id']] = cat['snippet']['title']
	df['categoryId'] = df['categoryId'].astype(str)
	df.insert(6,'category',df['categoryId'].map(id_vers_categorie))

	co = None
	try:
		co=psy.connect(host='berlin',database=userdb,user=user,password=pwd)

		curs = co.cursor()
	#######################
		print("\nTemps estimé de refonte de la base de données : 8min 30s")
		var=input("Refaire la base de données (O/n) ? ")
		if(var=='O' or var=='o' or var==1):
			print("Suppression des tables déjà existantes...")
			curs.execute('''DROP TABLE IF EXISTS Publier;
							DROP TABLE IF EXISTS Chaine;
							DROP TABLE IF EXISTS Video;
							DROP TABLE IF EXISTS Category;''')
	####################### Creation tables
			print("Création des tables...")
			curs.execute('''
							CREATE TABLE Categorie(
								idCategorie	numeric,
								nom varchar(30),
								CONSTRAINT pk_Categorie PRIMARY KEY (idCategorie)
							);
							CREATE TABLE Video(
								idVideo char(11),
								dateTendance date,
								titre varchar(300),
								dateSortie timestamp,
								vues numeric,
								likes numeric,
								dislikes numeric,
								commentaires numeric,
								categorie numeric,
								CONSTRAINT pk_Video PRIMARY KEY (idVideo, dateTendance),
								CONSTRAINT fk_Categorie FOREIGN KEY (categorie) REFERENCES Categorie(idCategorie)
							);
							CREATE TABLE Chaine(
								idChaine 	char(24),
								nom			varchar(100),
								CONSTRAINT pk_Chaine PRIMARY KEY (idChaine)
							);
							CREATE TABLE Publier(
								video char(11),
								dateTendance date,
								chaine char(24),
								CONSTRAINT pk_publier PRIMARY KEY (video,dateTendance,chaine),
								CONSTRAINT fk_chaine FOREIGN KEY (chaine) REFERENCES Chaine(idChaine),
								CONSTRAINT fk_video FOREIGN KEY (video, dateTendance) REFERENCES Video(idVideo, dateTendance)
							);
							''')


	####################### Insertion de données
			print("Insertion des données...")
			for row in df.itertuples():
				curs.execute('''INSERT INTO Video VALUES (%s,%s,%s,%s,%s,%s,%s,%s);''',
					(row.video_id,row.trending_date,row.title,row.publishedAt,row.view_count,row.likes,row.dislikes,row.comment_count))

				curs.execute('''INSERT INTO Chaine VALUES (%s,%s) ON CONFLICT ON CONSTRAINT pk_Chaine DO NOTHING;''',
					(row.channelId,row.channelTitle))

				curs.execute('''INSERT INTO Publier VALUES (%s,%s,%s);''',
					(row.video_id,row.trending_date,row.channelId))

				curs.execute('''INSERT INTO Categorie VALUES (%s,%s) ON CONFLICT ON CONSTRAINT pk_Categorie DO NOTHING;''',
					(row.categoryId,row.category))

	####################### Fin insertion
		co.commit()
		curs.close()
		print("Done")
	
	except(Exception,psy.DatabaseError) as error:
		print(error)
	finally:
		if co is not None:
			co.close()

user=input("Nom d'utilisateur : ")
pwd = getpass(prompt="Mot de passe : ")
userdb = "db" + user 
Table(user, userdb, pwd)
