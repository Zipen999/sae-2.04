SELECT DISTINCT c.nom
FROM Chaine c, Video v,Publier p
WHERE v.vues > 10000000
	AND c.idChaine = p.chaine
	AND p.video = v.idVideo;


SELECT DISTINCT v.dislikes,c.nom
FROM Video v,Publier p,Chaine c
WHERE c.idChaine = p.chaine
	AND p.video = v.idVideo
	AND v.dislikes >= ALL(SELECT v2.dislikes
						FROM Video v2);
-- MARCHE PAS
SELECT v.vues
FROM Video v
WHERE v.dateSortie <= '17-14-11'
	AND v.dateSortie >= '17-10-11';
	
-- MARCHE PAS
SELECT v.titre,v.likes/(v.likes+v.dislikes) as prcnt
FROM Video v
GROUP BY v.titre
ORDER BY prcnt;

-- Le nom et le nombre de vidéos de la chaine étant le plus apparu en tendances

SELECT c.nom, count(*) FROM Video v
INNER JOIN Publier p ON v.idVideo = p.Video AND v.dateTrending = p.dateTrending
INNER JOIN Chaine c ON c.idChaine = p.Chaine
GROUP BY c.nom 
HAVING count(*) >= ALL ( SELECT count(*) FROM Video v2
						INNER JOIN Publier p2 ON v2.idVideo = p2.Video AND v2.dateTrending = p2.dateTrending
						INNER JOIN Chaine c2 ON c2.idChaine = p2.Chaine
						GROUP BY c2.nom );

