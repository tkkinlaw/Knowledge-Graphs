MATCH (a:Aircraft)-[v:Visits]-(g:Grid50m)
WITH a, g, COLLECT(v) as visits
UNWIND visits AS visit
WITH a, g, visit, date(visit.Date_time) AS visitDate
ORDER BY a, g, visitDate
WITH a, g, COLLECT(visitDate) AS sortedVisits

// Identify the entities that are at the same place the next day
UNWIND RANGE(0, SIZE(sortedVisits) - 2) AS idx
WITH a, g, sortedVisits, idx, sortedVisits[idx] AS prevDate, sortedVisits[idx + 1] AS date, sortedVisits[idx + 2] AS postDate
WHERE prevDate IS NOT NULL AND postDate IS NOT NULL 
WITH a, g, prevDate, date, postDate, duration.between(prevDate, date).days AS daysBefore
WHERE daysBefore= 1
WITH a, g, prevDate, date, postDate, duration.between(date, postDate).days AS daysAfter
WHERE daysAfter= 1
RETURN a, g, prevDate, date, postDate

