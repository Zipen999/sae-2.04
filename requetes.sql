SELECT DISTINCT c.nom
FROM Chaine c, Video v,Publier p
WHERE v.vues > 10000000
	AND c.idChaine = p.chaine
	AND p.video = v.idVideo;


SELECT v.dislikes,c.nom
FROM Video v,Publier p,Chaine c
WHERE c.idChaine = p.chaine
	AND p.video = v.idVideo
	AND v.dislikes >= ALL(SELECT v2.dislikes
						FROM Video v2);

SELECT v.vues
FROM Video v
WHERE v.dateSortie <= '17-14-11'
	AND v.dateSortie >= '17-10-11';
