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

-- Le nom et le nombre de vidéos des 15 chaines étant le plus apparu en tendances

SELECT c.nom, count(*) AS NbVids
FROM Video v
	INNER JOIN Publier p ON v.idVideo = p.Video
	AND v.dateTrending = p.dateTrending
	INNER JOIN Chaine c ON c.idChaine = p.Chaine
	GROUP BY c.nom
	HAVING count(*)>=200
	ORDER BY NbVids DESC
	LIMIT 15;



-- Prcnt de likes et dislikes par rapport aux vues
SELECT titre, (likes+dislikes)/vues *100 AS prcnt FROM Video
	WHERE vues != 0 ORDER BY prcnt DESC;
