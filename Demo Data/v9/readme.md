### Data descriptions
The SupplyChainGeodatabase.xml includes:
- Distributors
- ProcessingPlants
- Products
- Products_messy
- Products_messy_backup (this is incase this demo needs resivited in class, since you modify the other file in the demo)
- Suppliers

The <code>Assign Parts to Product.ipynb</code> file appends "clean values" to the Products table. Then, this table was exported to Products_messy and manually obscured. 

The ContextualDataGeodatabase.xml includes:
- HurricanePath
- HurricanePath_buffer
- weather_reports_nlp (generated at the end of demo 3B)

## Knowledge Graphs:
### L3_EvaluateData_SupplyChain
- Use this KG for the Lesson 3A demo. 
- This KG contains clean and messy entities added for Product, Company, and SellsProduct entities & relationships
- This is the Knowledge graph feeding the two mapx files used in the demo: Structured Data Evaluation (Messy).mapx & Structured Data Evaluation (Clean).mapx

![SupplyChain](images/SupplyChain_Demo3A.png)
### SupplyChain
- Use this KG to for demos 1 & 4 Lesson 4. 
- It does not contain the Product, Company, and SellsProduct entities & relationships

![L3_SupplyChain](images/SupplyChain.png)
### SupplyChain_EndL4
- This is the KG created by the end of the lesson 4 demo.

![SupplyChain_L4End](images/SupplyChain_L4End.png)

To create this data on your machine, you will:
1. Create an ArcGIS Pro project on your VM. 
2. Add the KnowledgeGraphMagic.pyt to your project's toolboxes. 
3. Run the Create KG from JSON script. (See the notes above to determine which folder should be your input)
4. Create a new investigation in that project & point to the newly created KG in your portal.
5. If practicing demo 3a, you will need to import the 2 mapx files (which are link charts) into your project, and likely need to repair the paths to the KG service.