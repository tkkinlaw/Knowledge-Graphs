MATCH (a:Aircraft)-[v:Visits]-(g:Location)
WITH a, g, COLLECT(v) AS visits
RETURN a, g, visits