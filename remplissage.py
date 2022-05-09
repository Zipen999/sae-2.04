import pandas as pd
import psycopg2 as psy

from getpass import getpass

def Table(user, userdb, pwd):
	data=pd.read_csv(r'TrendingFR.csv')
	df=pd.DataFrame(data)
	df = df.drop_duplicates(subset=['video_id' , 'trending_date']) # Supprime les lignes dupliquées (Vidéos passés en tendances le même jour, impossible à traiter / incohérent sur youtube car une video peut passer en tendance une fois par jour)
	co = None
	try:
		co=psy.connect(host='berlin',database=userdb,user=user,password=pwd)

		curs = co.cursor()
	#######################
		print("Suppression des tables déjà existantes...")
		curs.execute('''DROP TABLE IF EXISTS Publier;
						DROP TABLE IF EXISTS Chaine;
						DROP TABLE IF EXISTS Video;''')
	####################### Creation tables
		print("Création des tables...")
		curs.execute('''CREATE TABLE Video(
								idVideo char(11),
								dateTrending date,
								titre varchar(300),
								dateSortie timestamp,
								vues numeric,
								likes numeric,
								dislikes numeric,
								commentaires numeric,
								CONSTRAINT pk_Video PRIMARY KEY (idVideo, dateTrending)
						);
						CREATE TABLE Chaine(
							idChaine 	char(24),
							nom			varchar(100),
							CONSTRAINT pk_Chaine PRIMARY KEY (idChaine)
						);
						CREATE TABLE Publier(
							video char(11),
							dateTrending date,
							chaine char(24),
							CONSTRAINT pk_publier PRIMARY KEY (video,dateTrending,chaine),
							CONSTRAINT fk_chaine FOREIGN KEY (chaine) REFERENCES Chaine(idChaine),
							CONSTRAINT fk_video FOREIGN KEY (video, dateTrending) REFERENCES Video(idVideo, dateTrending)
						);''')


	####################### Insertion de données
		print("Temps estimé d'insertion des données : 5min")
		var=input("Insérer les données (O/n) ? ")
		if(var=='o' or var=='O' or var==1):
			print("Insertion des données...")
			for row in df.itertuples():
				curs.execute('''INSERT INTO Video VALUES (%s,%s,%s,%s,%s,%s,%s,%s);''',
					(row.video_id,row.trending_date,row.title,row.publishedAt,row.view_count,row.likes,row.dislikes,row.comment_count))

				curs.execute('''INSERT INTO Chaine VALUES (%s,%s) ON CONFLICT ON CONSTRAINT pk_Chaine DO NOTHING;''',
					(row.channelId,row.channelTitle))

				curs.execute('''INSERT INTO Publier VALUES (%s,%s,%s);''',
					(row.video_id,row.trending_date,row.channelId))
	####################### Fin insertion
		co.commit()
		curs.close()
	
	except(Exception,psy.DatabaseError) as error:
		print(error)
	finally:
		if co is not None:
			co.close()

user=input("Nom d'utilisateur : ")
pwd = getpass(prompt="Mot de passe : ")
userdb = "db" + user 
Table(user, userdb, pwd)
