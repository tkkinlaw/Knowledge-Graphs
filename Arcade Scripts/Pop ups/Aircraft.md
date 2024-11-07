## Step 1
This is the base pop-up. Returns a list of AircraftIDs visiting a specific location, 17SNU0465097700.
```
var p = Portal('https://adsrv2019.ad.local/portal/')
var kg = KnowledgeGraphByPortalItem(p, 'cdfb76d077594fbab295644cc51a2fea')
var results = "MATCH (a:Aircraft)-[]-(g:Location{Grid:'17SNU0465097700'}) RETURN a.AircraftID"
var queryRes = QueryGraph(kg, results)
return queryRes
```

# Step 2
This variablizes the grid location to be the one the user clicks on. It requires the Arcade user to use bind parameters
```
var p = Portal('https://adsrv2019.ad.local/portal/')
var kg = KnowledgeGraphByPortalItem(p, 'cdfb76d077594fbab295644cc51a2fea')
var grid = $feature.Grid
var results = "MATCH (a:Aircraft)-[]-(g:Location{Grid:$Grid}) RETURN a.AircraftID"
var queryRes = QueryGraph(kg, results, {"Grid": grid})
return queryRes
```
