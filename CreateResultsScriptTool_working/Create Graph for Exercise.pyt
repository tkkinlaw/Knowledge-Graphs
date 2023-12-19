import arcpy
from arcgis.gis import GIS
from arcgis.graph import KnowledgeGraph
import os
import json
from datetime import datetime
from uuid import UUID

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Create Graph for Exercise"
        self.alias = "Create Graph for Exercise"

        # List of tool classes associated with this toolbox
        self.tools = [BackupKGAsJSON,CreateKGfromJSON]


class BackupKGAsJSON(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Backup Knowledge Graph as JSON"
        self.description = "This python script tool can be used within ArcGIS Pro to create a knowledge graph to begin an exercise. Use this tool if you did not complete an exercise properly. The JSON folder location is hard coded to: C:\backups\myknowledgegraph_backup"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""     
        gis = GIS("home")
        
        # Username
        paramUsername = arcpy.Parameter(
        displayName="Enterprise Portal Username",
        name="Enterprise_Portal_Username",
        datatype="GPString",
        parameterType="Required",
        direction="Input",
        category = "Connect to the GIS")

        # Password
        paramPassword = arcpy.Parameter(
        displayName="Enterprise Portal Password",
        name="Enterprise_Portal_Password",
        datatype="GPString",
        parameterType="Required",
        direction="Input",
        category = "Connect to the GIS")

        # Input KG to export to JSON files
        kgItems = [item for item in gis.content.search("type:Knowledge Graph", item_type="Knowledge Graph")]

        paramInputKG = arcpy.Parameter(
        displayName="Knowledge Graph to Export to JSON",
        name="Knowledge_Graph_to_Export_to_JSON",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        paramInputKG.filter.type = "ValueList"
        paramInputKG.filter.list = [item.url for item in kgItems]

        # Exercise number. For which lesson do you want to save a starting KG for, or create one for?
        paramExNum = arcpy.Parameter(
        displayName="Exercise Number",
        name="Exercise_number",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        paramExNum.filter.type = "ValueList"
        paramExNum.filter.list = ["1", "2", "3a", "3b"]

        # Output KG name
        paramOutKG = arcpy.Parameter(
        displayName="Output Knowledge Graph Name",
        name="Output_Knowledge_Graph_Name",
        datatype="GPString",
        parameterType="Required",
        direction="Output")

        # Declare output folder for JSON files
        paramJSONFolder = arcpy.Parameter(
        displayName="Folder Knowledge Graph Backups",
        name="Folder_Knowledge_Graph_Backups",
        datatype="GPString",
        parameterType="Required",
        direction="Output")
        paramJSONFolder.value = r"C:\backups\myknowledgegraph_backup"

        params = [paramUsername, paramPassword, paramExNum, paramInputKG, paramOutKG, paramJSONFolder]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Define folder and file names
        dm_ent = "datamodel_entities.json"
        dm_rel = "datamodel_relationships.json"
        all_ent = "all_entities.json"
        all_rel = "all_relationships.json"
        prov_file = "provenance_entities.json"  # this will only be used if you want to backup provenance records

        #Connect to the Enterprise Portal
        #url = arcpy.GetActivePortalURL()
        gis = GIS("home")
        knowledgegraph_backup = KnowledgeGraph(url=parameters[3].value, gis=gis)

        # Create backup files
        entity_types = []
        for types in knowledgegraph_backup.datamodel["entity_types"]:
            curr_entity_type = {
                "name": knowledgegraph_backup.datamodel["entity_types"][types]["name"],
                "properties": knowledgegraph_backup.datamodel["entity_types"][types]["properties"]}
            entity_types.append(curr_entity_type)

        folderPathRoot = os.path.join(parameters[5].value, parameters[2].value)
        if not os.path.exists(folderPathRoot):
            os.makedirs(folderPathRoot)
        with open(os.path.join(folderPathRoot, dm_ent), "w") as f:
            json.dump(entity_types, f)
        
        # Write data model relationship types to backup JSON file
        relationship_types = []
        for types in knowledgegraph_backup.datamodel["relationship_types"]:
            curr_relationship_type = {
                "name": knowledgegraph_backup.datamodel["relationship_types"][types]["name"],
                "properties": knowledgegraph_backup.datamodel["relationship_types"][types]["properties"]}
            relationship_types.append(curr_relationship_type)

        with open(os.path.join(folderPathRoot, dm_rel), "w") as f:
            json.dump(relationship_types, f)

        # Write entities to backup JSON file
        original_entities = knowledgegraph_backup.query_streaming("MATCH (n) RETURN distinct n")
        
        all_entities_fromquery = []
        for entity in list(original_entities):
            curr_entity = entity[0]
            # convert UUID values to a string since json can't store UUIDs
            curr_entity["_id"] = str(curr_entity["_id"])
            for prop in curr_entity["_properties"]:
                if type(curr_entity["_properties"][prop]) == UUID:
                    curr_entity["_properties"][prop] = str(curr_entity["_properties"][prop])
            # delete objectid, the server will handle creating new ones when we load the backup
            del curr_entity["_properties"]["objectid"]
            all_entities_fromquery.append(curr_entity)

        with open(os.path.join(folderPathRoot, all_ent), "w") as f:
            json.dump(all_entities_fromquery, f)
        
        # Write relationships to backup JSON file
        original_relationships = knowledgegraph_backup.query_streaming("MATCH ()-[rel]->() RETURN distinct rel")
        all_relationships_fromquery = []
        for relationship in list(original_relationships):
            curr_relationship = relationship[0]
            # convert UUID values to a string since json can't store UUIDs
            curr_relationship["_id"] = str(curr_relationship["_id"])
            curr_relationship["_originEntityId"] = str(curr_relationship["_originEntityId"])
            curr_relationship["_destinationEntityId"] = str(curr_relationship["_destinationEntityId"])
            for prop in curr_relationship["_properties"]:
                if type(curr_relationship["_properties"][prop]) == UUID:
                    curr_relationship["_properties"][prop] = str(curr_relationship["_properties"][prop])
            # delete objectid, the server will handle creating new ones when we load the backup
            del curr_relationship["_properties"]["objectid"]
            all_relationships_fromquery.append(curr_relationship)

        # OPTIONAL: Write provenance records to backup json file
        provenance_entities = knowledgegraph_backup.query_streaming("MATCH (n:Provenance) RETURN distinct n", include_provenance=True)

        with open(os.path.join(folderPathRoot, all_rel), "w") as f:
            json.dump(all_relationships_fromquery, f)

        # OPTIONAL: Write provenance records to backup JSON file
        provenance_entities = knowledgegraph_backup.query_streaming("MATCH (n:Provenance) RETURN distinct n", include_provenance=True)
        
        all_provenance_fromquery = []
        for entity in list(provenance_entities):
            curr_provenance = entity[0]
            # convert UUID values to a string since json can't store UUIDs
            curr_provenance["_id"] = str(curr_provenance["_id"])
            for prop in curr_provenance["_properties"]:
                if type(curr_provenance["_properties"][prop]) == UUID:
                    curr_provenance["_properties"][prop] = str(curr_provenance["_properties"][prop])
            # delete objectid, the server will handle creating new ones when we load the backup
            del curr_provenance["_properties"]["objectid"]
            all_provenance_fromquery.append(curr_provenance)

        with open(os.path.join(folderPathRoot, prov_file), "w") as f:
            json.dump(all_provenance_fromquery, f)

        # Load backup files
        result = gis.content.create_service(
        name=parameters[4].value,
        capabilities="Query,Editing,Create,Update,Delete",
        service_type="KnowledgeGraph")

        knowledgegraph_load = KnowledgeGraph(result.url, gis=gis)

        # Populate data model from saved JSON files
        with open(os.path.join(folderPathRoot, dm_ent), "r") as file:
            dm_ents = json.load(file)
        with open(os.path.join(folderPathRoot, dm_rel), "r") as file:
            dm_rels = json.load(file)
        knowledgegraph_load.named_object_type_adds(entity_types=dm_ents, relationship_types=dm_rels)
        
        # Get original document names to correctly load data
        doc_type_name = "Document"
        for entity_type in dm_ents:
            for prop in entity_type["properties"]:
                if entity_type["properties"][prop]["role"] == "esriGraphNamedObjectDocument":
                    doc_type_name = entity_type["name"]

        doc_rel_type_name = "HasDocument"
        for relationship_type in dm_rels:
            for prop in relationship_type["properties"]:
                if (relationship_type["properties"][prop]["role"] == "esriGraphNamedObjectDocument"):
                    doc_rel_type_name = relationship_type["name"]

        # Add additional document entity and relationship type properties
        origin_document_properties = None
        for entity_type in dm_ents:
            if entity_type["name"] == doc_type_name:
                origin_document_properties = entity_type["properties"]
        prop_list = []
        for prop in origin_document_properties:
            prop_list.append(origin_document_properties[prop])
        knowledgegraph_load.graph_property_adds(type_name="Document", graph_properties=prop_list)

        for relationship_type in dm_rels:
            if relationship_type["name"] == doc_rel_type_name:
                origin_document_rel_properties = relationship_type["properties"]
        prop_list = []
        for prop in origin_document_rel_properties:
            prop_list.append(origin_document_rel_properties[prop])
        knowledgegraph_load.graph_property_adds(type_name="HasDocument", graph_properties=prop_list)

        date_properties = []
        for types in dm_ents:
            for prop in types["properties"]:
                if types["properties"][prop]["fieldType"] == "esriFieldTypeDate":
                    date_properties.append(prop)

        for types in dm_rels:
            for prop in types["properties"]:
                if types["properties"][prop]["fieldType"] == "esriFieldTypeDate":
                    date_properties.append(prop)

        # Add all entities to the knowledge graph
        with open(os.path.join(folderPathRoot, all_ent), "r") as file:
            original_entities = json.load(file)
        batch = []
        for curr_entity in original_entities:
            if len(batch) > 20000:
                result = knowledgegraph_load.apply_edits(adds=batch)
                batch = []
                try:
                    print(result["error"])
                except:
                    print("No error adding entities")
            if curr_entity["_typeName"] == doc_type_name:
                curr_entity["_typeName"] = "Document"
            for prop in curr_entity["_properties"]:
                if prop in date_properties:
                    try:
                        curr_entity["_properties"][prop] = datetime.fromtimestamp(int(curr_entity["_properties"][prop] / 1000))
                    except:
                        curr_entity["_properties"][prop] = None
                try:
                    curr_entity["_properties"][prop] = UUID(curr_entity["_properties"][prop])
                except:
                    continue
            curr_entity["_id"] = UUID(curr_entity["_id"])
            batch.append(curr_entity)
        result = knowledgegraph_load.apply_edits(adds=batch)
        try:
            print(result["error"])
        except:
            print("No error adding entities")

        # Add all relationships to the knowledge graph
        with open(os.path.join(folderPathRoot, all_rel), "r") as file:
            original_rels = json.load(file)
        batch = []
        for curr_relationship in original_rels:
            # if a batch reaches 20k records, apply that batch of edits to the knowledge graph
            if len(batch) > 20000:
                result = knowledgegraph_load.apply_edits(adds=batch)
                batch = []
                # print error if one occurs during edit operation
                try:
                    print(result["error"])
                except:
                    print("No error adding relationships")
            # in case original document type name is different, change name to HasDocument
            if curr_relationship["_typeName"] == doc_rel_type_name:
                curr_relationship["_typeName"] = "HasDocument"
            # format UUID and date properties
            for prop in curr_relationship["_properties"]:
                if prop in date_properties:
                    try:
                        curr_relationship["_properties"][prop] = datetime.fromtimestamp(int(curr_relationship["_properties"][prop] / 1000))
                    except:
                        curr_relationship["_properties"][prop] = None
                try:
                    curr_relationship["_properties"][prop] = UUID(curr_relationship["_properties"][prop])
                except:
                    continue
            # format other relationship specific UUIDs
            curr_relationship["_id"] = UUID(curr_relationship["_id"])
            curr_relationship["_originEntityId"] = UUID(curr_relationship["_originEntityId"])
            curr_relationship["_destinationEntityId"] = UUID(curr_relationship["_destinationEntityId"])
            batch.append(curr_relationship)

        # apply final batch of edits to the knowledge graph
        if len(batch) > 2:
            result = knowledgegraph_load.apply_edits(adds=batch)
        # print error if one occurs during edit operation
        try:
            print(result["error"])
        except:
            print("No error adding relationships")

        # Add search indices to all text properties
        load_dm = knowledgegraph_load.datamodel
        # add search indexes for all entity text properties
        for entity_type in load_dm["entity_types"]:
            prop_list = []
            for prop in load_dm["entity_types"][entity_type]["properties"]:
                if (load_dm["entity_types"][entity_type]["properties"][prop]["fieldType"] == "esriFieldTypeString"):
                    prop_list.append(prop)
            knowledgegraph_load.update_search_index(adds={entity_type: {"property_names": prop_list}})

        for entity_type in load_dm["relationship_types"]:
            prop_list = []
            for prop in load_dm["relationship_types"][entity_type]["properties"]:
                if (load_dm["relationship_types"][entity_type]["properties"][prop]["fieldType"] == "esriFieldTypeString"):
                    prop_list.append(prop)
            knowledgegraph_load.update_search_index(
                adds={entity_type: {"property_names": prop_list}})

        # OPTIONAL: Add provenance records to the knowledge graph
        with open(os.path.join(folderPathRoot, prov_file), "r") as file:
            prov_entities = json.load(file)

        for curr_prov in prov_entities:
            # format UUID properties
            for prop in curr_prov["_properties"]:
                try:
                    curr_prov["_properties"][prop] = UUID(curr_prov["_properties"][prop])
                except:
                    continue
            # format id as UUID
            curr_prov["_id"] = UUID(curr_prov["_id"])
            # add provenance record
            knowledgegraph_load.apply_edits(adds=[curr_prov])
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

class CreateKGfromJSON(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Knowledge Graph from JSON"
        self.description = "This tool will create a Knowledge Graph from a folder of JSON files. This creates the entity types, relationship types, and loads the entities."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        gis = GIS("home")
        
        # Username
        paramUsername = arcpy.Parameter(
        displayName="Enterprise Portal Username",
        name="Enterprise_Portal_Username",
        datatype="GPString",
        parameterType="Required",
        direction="Input",
        category = "Connect to the GIS")

        # Password
        paramPassword = arcpy.Parameter(
        displayName="Enterprise Portal Password",
        name="Enterprise_Portal_Password",
        datatype="GPString",
        parameterType="Required",
        direction="Input",
        category = "Connect to the GIS")

        # Declare input folder for JSON files
        paramJSONFolder = arcpy.Parameter(
        displayName="Folder Knowledge Graph Backups",
        name="Folder_Knowledge_Graph_Backups",
        datatype="GPString",
        parameterType="Required",
        direction="Input")
        paramJSONFolder.value = r"C:\backups\myknowledgegraph_backup"

        # Exercise number. For which lesson do you want to save a starting KG for, or create one for?
        paramExNum = arcpy.Parameter(
        displayName="Exercise Number",
        name="Exercise_number",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        paramExNum.filter.type = "ValueList"
        paramExNum.filter.list = ["1", "2", "3a", "3b"]

        # Output KG name
        paramOutKG = arcpy.Parameter(
        displayName="Output Knowledge Graph Name",
        name="Output_Knowledge_Graph_Name",
        datatype="GPString",
        parameterType="Required",
        direction="Output")

        params = [paramUsername,paramPassword,paramJSONFolder,paramExNum,paramOutKG]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Define folder and file names
        dm_ent = "datamodel_entities.json"
        dm_rel = "datamodel_relationships.json"
        all_ent = "all_entities.json"
        all_rel = "all_relationships.json"
        prov_file = "provenance_entities.json"  # this will only be used if you want to backup provenance records

        # Connect to the GIS
        gis = GIS("home")

        # create a knowledge graph without provenance enabled
        result = gis.content.create_service(
        name=parameters[4].value,
        capabilities="Query,Editing,Create,Update,Delete",
        service_type="KnowledgeGraph")
        knowledgegraph_load = KnowledgeGraph(result.url, gis=gis)

        # load data model json files into graph data model
        folderPathRoot = os.path.join(parameters[2].value, parameters[3].value)
        with open(os.path.join(folderPathRoot, dm_ent), "r") as file:
            dm_ents = json.load(file)
        with open(os.path.join(folderPathRoot, dm_rel), "r") as file:
            dm_rels = json.load(file)
            knowledgegraph_load.named_object_type_adds(
            entity_types=dm_ents, relationship_types=dm_rels)

        # get document entity type name
        doc_type_name = "Document"
        for entity_type in dm_ents:
            for prop in entity_type["properties"]:
                if entity_type["properties"][prop]["role"] == "esriGraphNamedObjectDocument":
                    doc_type_name = entity_type["name"]
        
        # get document relationship type name
        doc_rel_type_name = "HasDocument"
        for relationship_type in dm_rels:
            for prop in relationship_type["properties"]:
                if (
                    relationship_type["properties"][prop]["role"]
                    == "esriGraphNamedObjectDocument"
                ):
                    doc_rel_type_name = relationship_type["name"]

        # load any additional document entity type properties
        origin_document_properties = None
        for entity_type in dm_ents:
            if entity_type["name"] == doc_type_name:
                origin_document_properties = entity_type["properties"]
        prop_list = []
        for prop in origin_document_properties:
            prop_list.append(origin_document_properties[prop])
        knowledgegraph_load.graph_property_adds(
            type_name="Document", graph_properties=prop_list
        )

        # load any additional document relationship type properties
        for relationship_type in dm_rels:
            if relationship_type["name"] == doc_rel_type_name:
                origin_document_rel_properties = relationship_type["properties"]
        prop_list = []
        for prop in origin_document_rel_properties:
            prop_list.append(origin_document_rel_properties[prop])
        knowledgegraph_load.graph_property_adds(
            type_name="HasDocument", graph_properties=prop_list
        )

        date_properties = []
        # add date property names for entity types
        for types in dm_ents:
            for prop in types["properties"]:
                if types["properties"][prop]["fieldType"] == "esriFieldTypeDate":
                    date_properties.append(prop)

        # add date property names for relationship types
        for types in dm_rels:
            for prop in types["properties"]:
                if types["properties"][prop]["fieldType"] == "esriFieldTypeDate":
                    date_properties.append(prop)

        # load entities json file
        with open(os.path.join(folderPathRoot, all_ent), "r") as file:
            original_entities = json.load(file)
        batch = []
        for curr_entity in original_entities:
            # if a batch reaches 20k records, apply that batch of edits to the knowledge graph
            if len(batch) > 20000:
                result = knowledgegraph_load.apply_edits(adds=batch)
                batch = []
                # print error if one occurs during edit operation
                try:
                    print(result["error"])
                except:
                    print("No error adding entities")
            # in case original document type name is different, change name to Document
            if curr_entity["_typeName"] == doc_type_name:
                curr_entity["_typeName"] = doc_type_name
            # format UUID and date properties
            for prop in curr_entity["_properties"]:
                if prop in date_properties:
                    try:
                        curr_entity["_properties"][prop] = datetime.fromtimestamp(
                            int(curr_entity["_properties"][prop] / 1000)
                        )
                    except:
                        curr_entity["_properties"][prop] = None
                try:
                    curr_entity["_properties"][prop] = UUID(curr_entity["_properties"][prop])
                except:
                    continue
            # format id UUID
            curr_entity["_id"] = UUID(curr_entity["_id"])
            batch.append(curr_entity)
        # apply final batch of edits to the knowledge graph
        result = knowledgegraph_load.apply_edits(adds=batch)
        # print error if one occurs during edit operation
        try:
            print(result["error"])
        except:
            print("No error adding entities")

        # load relationships json file
        with open(os.path.join(folderPathRoot, all_rel), "r") as file:
            original_rels = json.load(file)
        batch = []
        for curr_relationship in original_rels:
            # if a batch reaches 20k records, apply that batch of edits to the knowledge graph
            if len(batch) > 20000:
                result = knowledgegraph_load.apply_edits(adds=batch)
                batch = []
                # print error if one occurs during edit operation
                try:
                    print(result["error"])
                except:
                    print("No error adding relationships")
            # in case original document type name is different, change name to HasDocument
            if curr_relationship["_typeName"] == doc_rel_type_name:
                curr_relationship["_typeName"] = "HasDocument"
            # format UUID and date properties
            for prop in curr_relationship["_properties"]:
                if prop in date_properties:
                    try:
                        curr_relationship["_properties"][prop] = datetime.fromtimestamp(
                            int(curr_relationship["_properties"][prop] / 1000)
                        )
                    except:
                        curr_relationship["_properties"][prop] = None
                try:
                    curr_relationship["_properties"][prop] = UUID(
                        curr_relationship["_properties"][prop]
                    )
                except:
                    continue
            # format other relationship specific UUIDs
            curr_relationship["_id"] = UUID(curr_relationship["_id"])
            curr_relationship["_originEntityId"] = UUID(curr_relationship["_originEntityId"])
            curr_relationship["_destinationEntityId"] = UUID(
                curr_relationship["_destinationEntityId"]
            )
            batch.append(curr_relationship)
        # apply final batch of edits to the knowledge graph
        result = knowledgegraph_load.apply_edits(adds=batch)
        # print error if one occurs during edit operation
        try:
            print(result["error"])
        except:
            print("No error adding relationships")

        load_dm = knowledgegraph_load.datamodel
        # add search indexes for all entity text properties
        for entity_type in load_dm["entity_types"]:
            prop_list = []
            for prop in load_dm["entity_types"][entity_type]["properties"]:
                if (
                    load_dm["entity_types"][entity_type]["properties"][prop]["fieldType"]
                    == "esriFieldTypeString"
                ):
                    prop_list.append(prop)
            knowledgegraph_load.update_search_index(
                adds={entity_type: {"property_names": prop_list}}
            )

        # add search indexes for all relationship text properties
        for entity_type in load_dm["relationship_types"]:
            prop_list = []
            for prop in load_dm["relationship_types"][entity_type]["properties"]:
                if (
                    load_dm["relationship_types"][entity_type]["properties"][prop]["fieldType"]
                    == "esriFieldTypeString"
                ):
                    prop_list.append(prop)
            knowledgegraph_load.update_search_index(
                adds={entity_type: {"property_names": prop_list}}
            )

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return