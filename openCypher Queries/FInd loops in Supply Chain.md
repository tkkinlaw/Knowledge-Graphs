This openCypher query identifies paths that start and end in the same country, but use a foreign distributor
```cypher
// Supply chain paths that exit and re-enter the same country
MATCH path = (s:Supplier)-[:Supplies]->(d:Distributor)-[:SellsTo]->(p:ProcessingPlant), (cA:Country), (cB:Country)

// Supplier and Processing Plant in the same country (Country A)
WHERE esri.graph.ST_Intersects(s.shape, cA.shape)
AND esri.graph.ST_Intersects(p.shape, cA.shape)
// Distributor in a different country (Country B)
AND esri.graph.ST_Intersects(d.shape, cB.shape)
AND cA <> cB

RETURN path, cA.COUNTRY_NA AS originCountry, cB.COUNTRY_NA AS intermediaryCountry
```