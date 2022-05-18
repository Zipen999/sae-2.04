-- Le nom et le nombre de vidéos de la chaine étant le plus apparu en tendances

SELECT c.nom, count(*) AS NbVids FROM Video v
INNER JOIN Publier p ON v.idVideo = p.Video AND v.dateTendance = p.dateTendance
INNER JOIN Chaine c ON c.idChaine = p.Chaine
GROUP BY c.nom 
HAVING count(*)
ORDER BY NbVids
LIMIT 10;

-- Prcnt de likes et dislikes par rapport aux vues
SELECT titre, (likes+dislikes)/vues *100 AS prcnt FROM Video
	WHERE vues != 0 ORDER BY prcnt DESC;

-- Le jour de semaine ou il y a plus de nouvelle vidéos en tendance
SELECT to_char(v.dateSortie,'Day') AS Jour, count(*) AS Nb 
FROM Video v
GROUP BY Jour 
ORDER BY Nb DESC;

-- Les heures de publications les plus fréquentes.
SELECT to_char(v.dateSortie,'HH24') AS Heure, count(*) AS Nb
FROM Video v
GROUP BY Heure
ORDER BY Nb;

-- Les catégories les plus populaires
SELECT ca.nom , count(*) AS NbVids
FROM Video v
INNER JOIN Categorie ca ON ca.idCategorie = v.categorie
GROUP BY ca.idCategorie
ORDER BY NbVids DESC;

-- La video en tendence avec le moins de vues
SELECT min(v.vues)
FROM Video v
WHERE v.vues != 0;
