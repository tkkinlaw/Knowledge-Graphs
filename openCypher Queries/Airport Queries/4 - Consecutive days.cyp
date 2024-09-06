MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, COLLECT(v) AS visits
UNWIND visits AS visit
WITH a, g, visit, date(visit.Date_time) AS visitDate
ORDER BY a, g, visitDate
WITH a, g, COLLECT(visit) AS sortedVisits

UNWIND RANGE(0, SIZE(sortedVisits) - 2) AS idx
WITH a, g, sortedVisits, idx, sortedVisits[idx] AS day1, sortedVisits[idx + 1] AS day2, sortedVisits[idx + 2] AS day3
WITH a, g, sortedVisits, day1, day2, day3, 
  duration.between(date(day1.Date_time), date(day3.Date_time)).days AS timeSpan
WHERE timeSpan = 2
RETURN a, g, day1, day3, timeSpan