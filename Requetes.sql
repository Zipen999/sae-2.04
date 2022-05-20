-- Le nom et le nombre de vidéos de la chaine étant le plus apparu en tendances

SELECT c.nom, count(*) AS NbVids FROM Video v
INNER JOIN Publier p ON v.idVideo = p.Video AND v.dateTendance = p.dateTendance
INNER JOIN Chaine c ON c.idChaine = p.Chaine
GROUP BY c.nom 
HAVING count(*)
ORDER BY NbVids DESC
LIMIT 10;

-- Le jour de semaine ou il y a plus de nouvelle vidéos en tendance
SELECT to_char(v.dateSortie,'Day') AS Jour, count(*) AS Nb 
FROM Video v
GROUP BY Jour 
ORDER BY Nb DESC;

-- Les heures de publications les plus fréquentes.
SELECT to_char(v.dateSortie,'HH24') AS Heure, count(*) AS Nb
FROM Video v
GROUP BY Heure
ORDER BY Heure;
		
-- Les catégories les plus populaires
SELECT ca.nom , round((count(*) / ((SELECT count(*) FROM Video)*1.0)*100),2)
FROM Video v
INNER JOIN Categorie ca ON ca.idCategorie = v.categorie
WHERE ca.nom != 'NaN'
GROUP BY ca.idCategorie;

-- Categorie, likes, dislikes, sansavis
SELECT ca.nom AS Categorie, round((sum(v.likes)/sum(v.vues)*1.0)*100,2) AS LIKES, 
								round((sum(v.dislikes)/sum(v.vues)*1.0)*100,2) AS DISLIKES
								FROM Video v
								INNER JOIN categorie ca ON ca.idcategorie = v.categorie
								WHERE ca.nom != 'NaN'
								GROUP BY ca.idcategorie;
