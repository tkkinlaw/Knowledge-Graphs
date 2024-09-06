MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, COLLECT(v) AS visits
UNWIND visits AS visit
WITH a, g, visit, date(visit.Date_time) AS visitDate
ORDER BY a, g, visitDate
WITH a, g, COLLECT(visit) AS sortedVisits
RETURN a, g, sortedVisits
