## Step 1
This is the base pop-up. Returns a list of AircraftIDs visiting a specific location, 17SNU0465097700.
```
var p = Portal('https://adsrv2019.ad.local/portal/')
var kg = KnowledgeGraphByPortalItem(p, 'cdfb76d077594fbab295644cc51a2fea')
var results = "MATCH (a:Aircraft)-[]-(g:Location{Grid:'17SNU0465097700'}) RETURN a.AircraftID"
var queryRes = QueryGraph(kg, results)
return queryRes
```

## Step 2
This variablizes the grid location to be the one the user clicks on. It requires the Arcade user to use bind parameters
```
var p = Portal('https://adsrv2019.ad.local/portal/')
var kg = KnowledgeGraphByPortalItem(p, 'cdfb76d077594fbab295644cc51a2fea')
var grid = $feature.Grid
var results = "MATCH (a:Aircraft)-[]-(g:Location{Grid:$Grid}) RETURN a.AircraftID"
var queryRes = QueryGraph(kg, results, {"Grid": grid})
return queryRes
```

## Step 3
This uses the First function in Arcade to step inside the returned array containing an array.
```
var p = Portal('https://adsrv2019.ad.local/portal/')
var kg = KnowledgeGraphByPortalItem(p, 'cdfb76d077594fbab295644cc51a2fea')
var grid = $feature.Grid
var results = "MATCH (a:Aircraft)-[]-(g:Location{Grid:$Grid}) RETURN a.AircraftID"
var queryRes = QueryGraph(kg, results, {"Grid": grid})
return First(queryRes)
```

## Step 4
Clean the query results to get a single array, not an array of arrays
```var p = Portal('https://adsrv2019.ad.local/portal/')
var kg = KnowledgeGraphByPortalItem(p, 'cdfb76d077594fbab295644cc51a2fea')
var grid = $feature.Grid
var results = "MATCH (a:Aircraft)-[]-(g:Location{Grid:$Grid}) RETURN a.AircraftID"
var queryRes = QueryGraph(kg, results, {"Grid": grid})
var cleanRes = []
for(var index in queryRes) {
cleanRes = Splice(cleanRes, queryRes[index])
}
return cleanRes
```

## Step 5
Turn the array of arrays into a string
```
var p = Portal('https://adsrv2019.ad.local/portal/')
var kg = KnowledgeGraphByPortalItem(p, 'cdfb76d077594fbab295644cc51a2fea')
var grid = $feature.Grid
var results = "MATCH (a:Aircraft)-[]-(g:Location{Grid:$Grid}) RETURN a.AircraftID"
var queryRes = QueryGraph(kg, results, {"Grid": grid})
var cleanRes = []
for(var index in queryRes) {
cleanRes = Splice(cleanRes, queryRes[index])
}
var stringRes = ''
for(var index in cleanRes) {
stringRes += Text(cleanRes[index]) + ', '
}
return stringRes
```

## Step 6
Conditionally add a `', '` after the value. We don't want it if it's the last item.
```
var p = Portal('https://adsrv2019.ad.local/portal/')
var kg = KnowledgeGraphByPortalItem(p, 'cdfb76d077594fbab295644cc51a2fea')
var grid = $feature.Grid
var results = "MATCH (a:Aircraft)-[]-(g:Location{Grid:$Grid}) RETURN a.AircraftID"
var queryRes = QueryGraph(kg, results, {"Grid": grid})
var cleanRes = []
for(var index in queryRes) {
cleanRes = Splice(cleanRes, queryRes[index])
}
var stringRes = ''
var num = Count(cleanRes)
for(var index in cleanRes) {
stringRes += Text(cleanRes[index])
Iif(index != num-1, stringRes += ', ', '')
}
return stringRes
```