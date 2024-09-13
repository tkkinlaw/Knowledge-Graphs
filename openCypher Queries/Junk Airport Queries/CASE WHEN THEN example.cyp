MATCH (a:Aircraft)
WITH a,
CASE a.objectid
  WHEN 1 THEN 1
  WHEN 2 THEN 2
  ELSE 3
END AS objectID
RETURN a, objectID
