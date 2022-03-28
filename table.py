import pandas as pd
import psycopg2 as psy

data1 = pd.read_csv(r'characters.csv')
data2 = pd.read_csv(r'characterToComics.csv')
data3 = pd.read_csv(r'characters_stats.csv')
data4 = pd.read_csv(r'comics.csv')
data5 = pd.read_csv(r'marvel_characters_info.csv')

dfchar = pd.DataFrame(data1)
dfcharToCom = pd.DataFrame(data2)
dfcharStat = pd.DataFrame(data3)
dfcomic = pd.DataFrame(data4)
dfcharinfo = pd.DataFrame(data5)

df1 = dfchar.drop_duplicates()
df2 = dfcharToCom.drop_duplicates()
df3 = dfcharStat.drop_duplicates()
df4 = dfcomic.drop_duplicates()
df5 = dfcharinfo .drop_duplicates()

co = None


try:
	co = psy.connect(host='berlin',
					database='dblogin',
					user='login',
					password='mdp')

	curs = co.cursor()

	curs.execute('''DROP TABLE IF EXISTS Charactersstats;''')
  curs.execute('''DROP TABLE IF EXISTS Charchterinfo;''')
  curs.execute('''DROP TABLE IF EXISTS CharacterToComics;''')
  curs.execute('''DROP TABLE IF EXISTS Comics;''')
  curs.execute('''DROP TABLE IF EXISTS Charcacter;''')



	curs.execute('''CREATE TABLE Jeux(
						nom varchar(150),
						plateforme varchar(500),
						annee numeric(4),
						genre varchar(50),
						editeur varchar(50),
						venteNa numeric(5,2),
						venteEu numeric(5,2),
						venteJp numeric(5,2),
						venteAutre numeric(5,2),
						venteGlobale numeric(5,2),
						CONSTRAINT PK_Jeux PRIMARY KEY(nom,plateforme,annee)
						);''')


	for row in df2.itertuples():
		curs.execute('''INSERT INTO Jeux VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
