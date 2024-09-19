-----------------------------------------------
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
RETURN a, g, v
-----------------------------------------------
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
RETURN a, g, v
-----------------------------------------------
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
WITH a, g, collect(v) AS sortedVisits
RETURN a, g, sortedVisits
-----------------------------------------------
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
WITH a, g, collect(v) AS sortedVisits
UNWIND range(0, size(sortedVisits)-1) AS i
RETURN a, g, sortedVisits[i], i
-----------------------------------------------
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
WITH a, g, collect(v) AS sortedVisits
UNWIND range(0, size(sortedVisits)-1) AS i
WITH a, g, sortedVisits, i,
     duration.between(datetime(sortedVisits[i]['Date_time']),
          datetime(sortedVisits[i-1]['Date_time'])) AS prevDay,
     duration.between(datetime(sortedVisits[i+1]['Date_time']),
          datetime(sortedVisits[i]['Date_time'])) AS nextDay
RETURN a, g, prevDay, nextDay
-----------------------------------------------
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
WITH a, g, collect(v) AS sortedVisits
UNWIND range(0, size(sortedVisits)-1) AS i
WITH a, g, sortedVisits, i,
     duration.between(datetime(sortedVisits[i]['Date_time']),
          datetime(sortedVisits[i-1]['Date_time'])) AS prevDay,
     duration.between(datetime(sortedVisits[i+1]['Date_time']),
          datetime(sortedVisits[i]['Date_time'])) AS nextDay
WHERE (prevDay.days = 0 OR nextDay.days = 0)
RETURN a, g, prevDay, nextDay
-----------------------------------------------
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
WITH a, g, collect(v) AS sortedVisits
UNWIND range(0, size(sortedVisits)-1) AS i
WITH a, g, sortedVisits, i,
     duration.between(datetime(sortedVisits[i]['Date_time']),
          datetime(sortedVisits[i-1]['Date_time'])) AS prevDay,
     duration.between(datetime(sortedVisits[i+1]['Date_time']),
          datetime(sortedVisits[i]['Date_time'])) AS nextDay
WHERE (prevDay.days = 0 OR nextDay.days = 0)
  AND (prevDay.hours <> 0 AND nextDay.hours <> 0) //<- Why is this needed?
WITH a, g, collect(sortedVisits[i]) AS results
WHERE size(results) >= 3
RETURN a, g, results