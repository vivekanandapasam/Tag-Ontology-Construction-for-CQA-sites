# Tag-Ontology-Construction-for-CQA-sites
Constructing Tag onotlogy for QA sites

# Description of what each folder and files contains
1. datacsv - Contains csv files of posts and tags which are creates from xml files in super meta folder. It also creates nodes.csv and edges.csv which are created from Ontology.py file.

2. xml_to_csv - Converts the xml files in super meta folder to csv files

3. model - labelled LDA model

4. cleandata.py - reads the csv files in datacsv and created dictionaries of posts and tags

5. Ontology.py - creates edges for all the tags and saves common and similarity pickles(comm.p and sim.p) to the disk

