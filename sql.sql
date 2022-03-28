DROP TABLE IF EXISTS Characters;
DROP TABLE IF EXISTS CharactersInfo;
DROP TABLE IF EXISTS CharactersStats;
DROP TABLE IF EXISTS CharactersToComics;
DROP TABLE IF EXISTS Comics;

CREATE TABLE Characters(
	idChar char(7) PRIMARY KEY,
	Nom varchar(30)
);

CREATE TABLE CharactersInfo(
	Nom			char(25),
	Alignement	char(8),
	Sexe		
	CouleurYeux
	Race
	CouleurCheveux
	Editeur
	CouleurDePeau
	Taille
	Poids
	CONSTRAINT ck_alig CHECK Alignement IN ('Bon' OR 'Mauvais'),

);