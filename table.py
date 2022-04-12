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

	curs.execute('''DROP TABLE IF EXISTS Video;''')
  	curs.execute('''DROP TABLE IF EXISTS Channel;''')
 	curs.execute('''DROP TABLE IF EXISTS Category;''')



	curs.execute('''CREATE TABLE Video(
					idVideo char() PRIMARY KEY,
					titre varchar(300),
					dateSortie date,
					vues numeric,
					likes numeric,
					dislikes numeric,
					commentaires numeric,
						);''')
	curs.execute('''CREATE TABLE Publier(
					idVideo char() PRIMARY KEY,
					idChaine varchar() PRIMARY KEY,
						);''')
	
	curs.execute('''CREATE TABLE Chaine(
					idChannel varchar() PRIMARY KEY,
					nom
						
						);''')
	
	
	curs.execute('''CREATE TABLE Appartenir(
					
						
						);''')


	for row in df2.itertuples():
		curs.execute('''INSERT INTO Jeux VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
