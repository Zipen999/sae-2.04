SELECT c.nom
FROM Chaine c, Video v,Publier p
WHERE v.vues > 10000000
	AND c.idChaine = p.chaine
	AND p.video = v.idVideo;


SELECT MAX(v.dislikes),v.titre,
FROM Video v
WHERE v.dateSortie = CURRENT_DATE-5*365;
