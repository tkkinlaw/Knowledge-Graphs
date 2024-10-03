----------------------------------------------- 1
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
RETURN a, g, v
----------------------------------------------- 1a
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
RETURN count(DISTINCT a) , count(DISTINCT g), count(DISTINCT v)
----------------------------------------------- 2
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
RETURN a, g, v
----------------------------------------------- 2a
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
RETURN a, g, datetime(v.Date_time)
----------------------------------------------- 3
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
WITH a, g, collect(v) AS sortedVisits
RETURN a, g, sortedVisits
----------------------------------------------- 3a
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
WITH a, g, collect(v.Date_time) AS sortedVisits
RETURN a, g, sortedVisits
----------------------------------------------- 4 & 1
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
WITH a, g, collect(v) AS sortedVisits
UNWIND range(0, size(sortedVisits)-1) AS i
RETURN a, g, sortedVisits[i], i
----------------------------------------------- 5 
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
----------------------------------------------- 5a
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
WITH a, g, collect(v) AS sortedVisits
UNWIND range(0, size(sortedVisits)-1) AS i
WITH a, g, sortedVisits, i,
     datetime(sortedVisits[i]['Date_time']) AS currDay,
     datetime(sortedVisits[i-1]['Date_time']) AS prevDay,
     datetime(sortedVisits[i+1]['Date_time']) AS nextDay
RETURN a, g, duration.Between(currDay, nextDay).hours AS Hours, currDay, nextDay
----------------------------------------------- 5b
MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
ORDER BY datetime(v.Date_time)
WITH a, g, collect(v) AS sortedVisits
UNWIND range(0, size(sortedVisits)-1) AS i
WITH a, g, sortedVisits, i,
     datetime(sortedVisits[i]['Date_time']) AS currDay,
     datetime(sortedVisits[i-1]['Date_time']) AS prevDay,
     datetime(sortedVisits[i+1]['Date_time']) AS nextDay
RETURN a, g, duration.Between(currDay, nextDay).days AS Days, currDay, nextDay
----------------------------------------------- 6
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
----------------------------------------------- 6a
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
RETURN a, g, prevDay.days, nextDay.days
----------------------------------------------- 7
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
WITH a, g, collect(sortedVisits[i]) AS results
WHERE size(results) >= 3
RETURN a, g, results
----------------------------------------------- 7a
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
WITH a, g, collect(sortedVisits) AS results
RETURN a, g, results
----------------------------------------------- 8
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
WITH a, g, collect(sortedVisits[i]) AS results
WHERE size(results) >= 3
RETURN a, g, results