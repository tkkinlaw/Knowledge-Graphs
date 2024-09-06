MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, COLLECT(v) AS visits
UNWIND visits AS visit
WITH a, g, visit, date(visit.Date_time) AS visitDate
ORDER BY a, g, visitDate
WITH a, g, COLLECT(visitDate) AS sortedVisitDates
UNWIND RANGE(0, SIZE(sortedVisitDates) - 1) AS i
WITH a, g, sortedVisitDates, i
WHERE sortedVisitDates[i] = sortedVisitDates[i - 1] + duration('P1D')
RETURN a, g, COLLECT(sortedVisitDates[i])