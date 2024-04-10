# Variables
inputKG = 'af633f950ed5408caa2a146f0c564e44' #item ID
targetKG = '5c43bc7def3b4c1cb8b5ddef3d640c20' #item ID
resourcePath = r'C:\Users\tim10393\Downloads\sandbox' #folder to other JSON files

from arcgis.gis import GIS
import json
import os

gis = GIS('Pro', verify_cert=False)

inputKG = gis.content.get(inputKG)
inputKG

# Format items as JSON & Dictionary
prop = {
    "title":inputKG.title,
    "description": inputKG.description,
    "snippet": inputKG.snippet,
    "tags": inputKG.tags
}
prop

# Convert and write JSON object to file
outData = os.path.join(resourcePath,"itemDetails.json")
with open(outData, "w") as outfile: 
    json.dump(prop, outfile)

inputKG.download_thumbnail(resourcePath)

inData = os.path.join(resourcePath, "itemDetails.json")
with open(inData, 'r') as infile:
    jItemDetails = json.load(infile)
jItemDetails

targetItem = gis.content.get(targetKG)
targetItem

with arcpy.EnvManager(workspace=resourcePath):
    thumbnail = os.path.join(resourcePath, arcpy.ListRasters()[0])

targetItem.update(item_properties = jItemDetails, thumbnail = thumbnail)

targetItem


