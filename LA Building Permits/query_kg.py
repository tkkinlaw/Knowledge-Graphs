"""
Query Knowledge Graph Server for LA Building Permits using ArcGIS API for Python
"""

from arcgis.features import KnowledgeGraph

def main():
    # Connect to the Knowledge Graph Server
    kg = KnowledgeGraph(
        url='https://ebase.ad.local/server/rest/services/Hosted/LA_Building_Permits/KnowledgeGraphServer'
    )
    
    # Execute the openCypher query
    query = 'MATCH (c:Contractor) RETURN c.ContractorBusinessName'
    print(f"Executing query: {query}\n")
    
    try:
        results = kg.query(query)
        
        # Display results
        print("Query Results:")
        print("-" * 50)
        if results:
            for row in results:
                print(row)
        else:
            print("No results returned")
            
    except Exception as e:
        print(f"Error executing query: {e}")

if __name__ == "__main__":
    main()
