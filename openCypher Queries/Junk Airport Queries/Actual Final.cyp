MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, v
    ORDER BY DATE(v.Date_time)
WITH a, g, 
    COLLECT(v) AS sortedVisits
UNWIND RANGE(0, SIZE(sortedVisits) - 1) AS i
WITH a, g, sortedVisits, i
    WHERE DATE(sortedVisits[i]['Date_time']) = DATE(sortedVisits[i - 1]['Date_time']) + duration('P1D')
WITH a, g, COLLECT(sortedVisits[i]) AS results
RETURN a, g, results

// I was trying to do sortedVisits[i].Date_time, but it wasn't working
// I think when collecting, unwinding items, it becomes a map and not a entity or relationship...which may be why sortedVisits[i]['Date_time'] works. 
//properties(sortedVisits[i]) returns all properties fine
// duration.between(Date(sortedVisits[i]['Date_time']), Date(sortedVisits[i+1]['Date_time'])).days