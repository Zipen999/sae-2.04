import pandas as pd
import psycopg2 as psy

from getpass import getpass

def Table(user, userdb, pwd):
	data=pd.read_csv(r'TrendingFR.csv')
	df=pd.DataFrame(data)
	df = df.drop_duplicates(subset=['video_id' , 'trending_date']) # Supprime les lignes dupliqués
	co = None
	try:
		co=psy.connect(host='berlin',database=userdb,user=user,password=pwd)

		curs = co.cursor()
	#######################
		curs.execute('''DROP TABLE IF EXISTS Publier;
						DROP TABLE IF EXISTS Chaine;
						DROP TABLE IF EXISTS Video;''')
	####################### Creation tables
		curs.execute('''CREATE TABLE Video(
								idVideo char(11),
								dateTrending date,
								titre varchar(300),
								dateSortie date,
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
		for row in df.itertuples():
			curs.execute('''INSERT INTO Video VALUES (%s,%s,%s,%s,%s,%s,%s,%s);''',
				(row.video_id,row.trending_date,row.title,row.publishedAt,row.view_count,row.likes,row.dislikes,row.comment_count))

			curs.execute('''INSERT INTO Chaine VALUES (%s,%s) ON CONFLICT ON CONSTRAINT pk_Chaine DO NOTHING;''',
				(row.channelId,row.channelTitle))

			curs.execute('''INSERT INTO Publier VALUES (%s,%s,%s);''',
				(row.video_id,row.trending_date,row.channelId))
		co.commit()
		curs.close()
	
	except(Exception,psy.DatabaseError) as error:
		print(error)
	finally:
		if co is not None:
			co.close()

user=input("Nom d'utilisateur : ")
pwd = getpass()
userdb = "db" + user 
Table(user, userdb, pwd)
